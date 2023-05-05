from django.utils.translation import gettext as _

TEXT_QUESTION_TYPE_SHORT = 0
TEXT_QUESTION_TYPE_LONG = 1

TEXT_QUESTION_TYPES = (
    (TEXT_QUESTION_TYPE_SHORT, _("short")),
    (TEXT_QUESTION_TYPE_LONG, _("long")),
)