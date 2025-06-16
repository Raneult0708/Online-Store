from django.shortcuts import render

# Create your views here.
def accueil(request):
    return render(request, 'accueil.html')
def profil(request):
    return render(request, 'profil.html')
def sign_up(request):
    return render(request, 'sign_up.html')
def publish_ride(request):
    return render(request, 'publish_ride.html')




#===========================CHAT===============================

@login_required_custom
def chat_home(request):
    """Page principale du chat"""
    utilisateur_actuel = get_current_user(request)
    
    # Calculer les initiales
    user_initials = 'U'
    if utilisateur_actuel and utilisateur_actuel.nom:
        words = utilisateur_actuel.nom.strip().split()
        if len(words) == 1:
            user_initials = words[0][0].upper()
        else:
            user_initials = (words[0][0] + words[-1][0]).upper()
    
    # Récupérer toutes les conversations de l'utilisateur
    conversations = Conversation.objects.filter(
        models.Q(owner=utilisateur_actuel) | 
        models.Q(participants=utilisateur_actuel)
    ).distinct().order_by('-date_creation')
    
    
    # Préparer les données pour le template
    conversations_data = []
    for conv in conversations:
        nom_affichage = conv.get_nom_affichage(utilisateur_actuel)
        # Calculer les initiales
        words = nom_affichage.split()
        if len(words) == 1:
            initiales = words[0][0].upper()
        else:
            initiales = (words[0][0] + words[-1][0]).upper()
        conversations_data.append({
            'id': conv.id,
            'nom_affichage': nom_affichage,
            'initiales': initiales,
            'dernier_message': conv.dernier_message(),
            'messages_non_lus': conv.messages_non_lus(utilisateur_actuel),
            'date_creation': conv.date_creation
            })
    
    return render(request, 'commun/message.html', {
        'conversations': conversations,
        'utilisateur_actuel': utilisateur_actuel,
        'user_initials': user_initials  # Ajouter les initiales
    })

@login_required_custom
def get_conversation_messages(request, conversation_id):
    """Récupérer les messages d'une conversation"""
    utilisateur_actuel = get_current_user(request)
    
    # Vérifier que l'utilisateur a accès à cette conversation
    conversation = get_object_or_404(
        Conversation.objects.filter(
        models.Q(owner=utilisateur_actuel) | 
        models.Q(participants=utilisateur_actuel),
        id=conversation_id            
        )
    )
    
    last_message_id = request.GET.get('last_id', 0)
    
    # Récupérer les nouveaux messages
    messages_query = Message.objects.filter(
        conversation=conversation,
        id__gt=last_message_id
    ).order_by('date_envoi')
    
    # Préparer les données pour JSON
    messages_data = []
    for msg in messages_query:
        messages_data.append({
            'id': msg.id,
            'expediteur': msg.expediteur.nom if hasattr(msg.expediteur, 'nom') else 'Utilisateur',
            'contenu': msg.contenu,
            'date_envoi': msg.date_envoi.strftime('%H:%M') if msg.date_envoi else '',
            'est_mien': msg.expediteur.id == utilisateur_actuel.id
        })
    
    return JsonResponse({'messages': messages_data})

@csrf_exempt
@login_required_custom
def envoyer_message(request):
    """Envoyer un nouveau message"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
    
    try:
        data = json.loads(request.body)
        conversation_id = data.get('conversation_id')
        contenu = data.get('contenu', '').strip()
        
        if not contenu:
            return JsonResponse({'error': 'Le message ne peut pas être vide'}, status=400)
        
        utilisateur_actuel = get_current_user(request)
        
        # Vérifier que l'utilisateur a accès à cette conversation
        conversation = get_object_or_404(
            Conversation.objects.filter(
            models.Q(owner=utilisateur_actuel) | 
            models.Q(participants=utilisateur_actuel),
            id=conversation_id
            )
        )
        
        # Créer le message
        message = Message.objects.create(
            conversation=conversation,
            expediteur=utilisateur_actuel,
            contenu=contenu,
            date_envoi=timezone.now()
        )
        
        # Retourner les données du message
        return JsonResponse({
            'id': message.id,
            'expediteur': message.expediteur.nom if hasattr(message.expediteur, 'nom') else 'Utilisateur',
            'contenu': message.contenu,
            'date_envoi': message.date_envoi.strftime('%H:%M'),
            'est_mien': True
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Données JSON invalides'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required_custom
def creer_conversation(request):
    """Créer une nouvelle conversation"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nom_conversation = data.get('nom', '')
            participants_ids = data.get('participants', [])
            
            utilisateur_actuel = get_current_user(request)
            
            # Créer la conversation
            conversation = Conversation.objects.create(
                nom=nom_conversation,
                owner=utilisateur_actuel,
                date_creation=timezone.now()
            )
            
            # Ajouter les participants
            if participants_ids:
                participants = Utilisateur.objects.filter(id__in=participants_ids)
                conversation.participants.set(participants)
            
            # Ajouter l'owner comme participant
            conversation.participants.add(utilisateur_actuel)
            
            return JsonResponse({
                'id': conversation.id,
                'nom': conversation.get_nom_affichage(utilisateur_actuel),
                'success': True
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@login_required_custom
def rechercher_utilisateur(request):
    """Rechercher un utilisateur par email pour créer une conversation"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email', '').strip()
            
            if not email:
                return JsonResponse({'error': 'Email requis'}, status=400)
            
            try:
                utilisateur = Utilisateur.objects.get(email=email)
                utilisateur_actuel = get_current_user(request)
                
                # Vérifier qu'on ne recherche pas soi-même
                if utilisateur.id == utilisateur_actuel.id:
                    return JsonResponse({'error': 'Vous ne pouvez pas vous envoyer un message à vous-même'}, status=400)
                
                # Vérifier s'il existe déjà une conversation
                conversation_existante = Conversation.objects.filter(
                    models.Q(owner=utilisateur_actuel, participants=utilisateur) |
                    models.Q(owner=utilisateur, participants=utilisateur_actuel)
                ).first()
                
                if conversation_existante:
                    return JsonResponse({
                        'conversation_id': conversation_existante.id,
                        'nom': conversation_existante.get_nom_affichage(utilisateur_actuel),
                        'existe_deja': True
                    })
                
                # Créer nouvelle conversation
                conversation = Conversation.objects.create(
                    owner=utilisateur_actuel,
                    date_creation=timezone.now()
                )
                conversation.participants.add(utilisateur_actuel, utilisateur)
                
                return JsonResponse({
                    'conversation_id': conversation.id,
                    'nom': conversation.get_nom_affichage(utilisateur_actuel),
                    'existe_deja': False,
                    'success': True
                })
                
            except Utilisateur.DoesNotExist:
                return JsonResponse({'error': 'Aucun utilisateur trouvé avec cet email'}, status=404)
                
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Données JSON invalides'}, status=400)
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)