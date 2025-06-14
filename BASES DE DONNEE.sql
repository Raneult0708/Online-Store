-- Fichier: schema_ifri_comotorage.sql

-- Désactiver temporairement la vérification des clés étrangères pour faciliter l'ordre de création
SET FOREIGN_KEY_CHECKS = 0;

CREATE TABLE Utilisateur (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    numero_telephone VARCHAR(20) UNIQUE NOT NULL, 
    email VARCHAR(255) UNIQUE NOT NULL,           
    mot_de_passe VARCHAR(255) NOT NULL,      
    est_conducteur BOOLEAN,
    photo_profil VARCHAR(255)
);

CREATE TABLE Vehicule (
    id INT AUTO_INCREMENT PRIMARY KEY,
    utilisateur_id INT NOT NULL, 
    marque VARCHAR(100) NOT NULL,
    modele VARCHAR(100) NOT NULL,
    places_disponibles INT NOT NULL,
    FOREIGN KEY (utilisateur_id) REFERENCES Utilisateur(id)
);

CREATE TABLE OffreCovoiturage (
    id INT AUTO_INCREMENT PRIMARY KEY,
    conducteur_id INT NOT NULL,
    point_depart VARCHAR(255) NOT NULL,    
    point_arrivee VARCHAR(255) NOT NULL,  
    heure_depart DATETIME NOT NULL,        
    places_disponibles INT NOT NULL,       
    date_publication DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conducteur_id) REFERENCES Utilisateur(id)
);

CREATE TABLE DemandeCovoiturage (
    id INT AUTO_INCREMENT PRIMARY KEY,
    passager_id INT NOT NULL,
    point_depart VARCHAR(255) NOT NULL,    
    point_arrivee VARCHAR(255) NOT NULL,   
    heure_depart_souhaitee DATETIME NOT NULL, 
    date_publication DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (passager_id) REFERENCES Utilisateur(id)
);

-- Table des Conversations (pour la messagerie)
CREATE TABLE Conversation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    owner_id INT NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES Utilisateur(id)
);

-- Table des Messages
CREATE TABLE Message (
    id INT AUTO_INCREMENT PRIMARY KEY,
    conversation_id INT NOT NULL,
    expediteur_id INT NOT NULL,
    contenu TEXT NOT NULL,
    date_envoi DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES Conversation(id),
    FOREIGN KEY (expediteur_id) REFERENCES Utilisateur(id)
);

CREATE TABLE rides (
    id INT PRIMARY KEY AUTO_INCREMENT,
    conducteur_id INT NOT NULL,
    FOREIGN KEY (conducteur_id) REFERENCES Utilisateur(id),
    vehicule_id INT NULL,
    FOREIGN KEY (vehicule_id) REFERENCES Vehicule(id),
    point_depart VARCHAR(500) NOT NULL,
    point_arrivee VARCHAR(500) NOT NULL,
    latitude_depart DECIMAL(10, 8) NOT NULL,
    longitude_depart DECIMAL(11, 8) NOT NULL,
    latitude_arrivee DECIMAL(10, 8) NOT NULL,
    longitude_arrivee DECIMAL(11, 8) NOT NULL,
    heure_depart DATETIME NOT NULL,
    heure_arrivee_prevue DATETIME NULL,
    nb_places_disponibles INT NOT NULL,
    description TEXT NULL,
    statut ENUM('active', 'complete', 'cancelled', 'not_started') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE bookings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    ride_id INT NOT NULL,
    FOREIGN KEY (ride_id) REFERENCES rides(id),
    passager_id INT NOT NULL,
    FOREIGN KEY (passager_id) REFERENCES Utilisateur(id),
    nb_places_reservees INT DEFAULT 1,
    statut ENUM('pending', 'confirmed', 'cancelled', 'completed') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE matching_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    ride_id INT NOT NULL,
    request_id INT NOT NULL,
    score_compatibilite DECIMAL(5, 2) NOT NULL,
    distance_km DECIMAL(8, 2) NOT NULL,
    difference_horaire_minutes INT NOT NULL,
    statut ENUM('proposed', 'accepted', 'rejected') DEFAULT 'proposed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ride_id) REFERENCES rides(id),
    FOREIGN KEY (request_id) REFERENCES DemandeCovoiturage(id)
);

-- Réactiver la vérification des clés étrangères
SET FOREIGN_KEY_CHECKS = 1;
