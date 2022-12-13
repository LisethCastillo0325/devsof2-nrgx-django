# Django
from django.core.validators import RegexValidator


class CellNumberRegexValidator(RegexValidator):

    def __init__(self, message=None, code=None, inverse_match=None, flags=None):
        super().__init__(
            regex=(
                r"^(300|301|302|303|304|324|305|310|311|312|313|314|320|321|"
                r"322|323|315|316|317|318|319|319|350|351|302|323|324|324|333)[0-9]{7}"
            ),
            message=message,
            code=code,
            inverse_match=inverse_match,
            flags=flags
        )
