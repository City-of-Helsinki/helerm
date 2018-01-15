import pytest

from metarecord.models import Action, Function, Phase, Record


@pytest.mark.parametrize('model', [Action, Function, Phase, Record])
def test_allowed_contains_required_keys(model):
    required_keys = set(model._attribute_validations.get('required', {})) | set(
        model._attribute_validations.get('conditionally_required', {}).keys())

    assert set(model._attribute_validations['allowed']).issuperset(required_keys), \
        'allowedKeys does not contain all the required keys in the model "{}" attribute validations'.format(
            model.__name__)
