import random

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django_namespaces import loaders
from django_namespaces.models import Reaction, ReactionStatus, ReactionType

ReactionStatus = loaders.ReactionStatus
ReactionType = loaders.ReactionType

REACTION_CHOICES = ReactionType.choices
REACTION_DEFAULT = ReactionType.get_default()

class ReactionTestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        user_count = 2
        for i in range(user_count):
            User.objects.create_user(f"django_namespaces_user_{i}", password=f'testpassword-{i}')
        users = User.objects.all().order_by("?")
        self.user_a = users.first()
        self.user_b = users.last()
        content_type = ContentType.objects.get_for_model(User)
        self.default_reaction = Reaction.objects.create(user=self.user_a, content_type=content_type, object_id=self.user_b.pk)
        default_args = {
            "user": self.user_a,
            "content_type": content_type,
            "object_id": self.user_b.pk,
        }
        self.active_love = Reaction(status=ReactionStatus.ACTIVE, reaction=ReactionType.LOVE, **default_args)
        self.active_hate = Reaction(status=ReactionStatus.ACTIVE, reaction=ReactionType.HATE, **default_args)
        self.inactive_cool = Reaction(status=ReactionStatus.INACTIVE, reaction=ReactionType.COOL, **default_args)
        self.inactive_wow = Reaction(status=ReactionStatus.INACTIVE, reaction=ReactionType.WOW, **default_args)
        self.active_thumbs_up = Reaction(status=ReactionStatus.ACTIVE, reaction=ReactionType.THUMBS_UP, **default_args)
        self.active_thumbs_down = Reaction(status=ReactionStatus.ACTIVE, reaction=ReactionType.THUMBS_DOWN, **default_args)
        # Save the reactions to the database
        self.active_love.save()
        self.active_hate.save()
        self.inactive_cool.save()
        self.inactive_wow.save()
        self.active_thumbs_up.save()
        self.active_thumbs_down.save()
        self.reaction_count = 7


    def test_total_reactions(self):
        qs = Reaction.objects.all()
        self.assertTrue(qs.exists())
        self.assertEqual(qs.count(), self.reaction_count)

      # Test the default values of the reaction fields
    def test_default_reaction_values(self):
        self.assertEqual(self.default_reaction.reaction, REACTION_DEFAULT)
        self.assertEqual(self.default_reaction.status, ReactionStatus.ACTIVE)
        self.assertTrue(self.default_reaction.is_active)
        self.assertFalse(self.default_reaction.is_inactive)

    # Test the ReactionManager methods
    def test_reaction_manager_methods(self):
        # Test the active() method
        active_reactions = Reaction.objects.active().order_by("pk")
        self.assertQuerysetEqual(active_reactions, [self.default_reaction, self.active_love, self.active_hate, self.active_thumbs_up, self.active_thumbs_down], 
                                 transform=lambda x: x)

        # Test the inactive() method
        inactive_reactions = Reaction.objects.inactive().order_by("pk")
        self.assertQuerysetEqual(inactive_reactions, [self.inactive_cool, self.inactive_wow], 
                                 transform=lambda x: x)

        # Test the by_reaction() method
        love_reactions = Reaction.objects.by_reaction(ReactionType.LOVE).order_by("pk")
        self.assertQuerysetEqual(love_reactions, [self.default_reaction, self.active_love], 
                                 transform=lambda x: x)

        hate_reactions = Reaction.objects.by_reaction(ReactionType.HATE).order_by("pk")
        self.assertQuerysetEqual(hate_reactions, [self.active_hate], 
                                 transform=lambda x: x)

        cool_reactions = Reaction.objects.by_reaction(ReactionType.COOL).order_by("pk")
        self.assertQuerysetEqual(cool_reactions, [self.inactive_cool], 
                                 transform=lambda x: x)