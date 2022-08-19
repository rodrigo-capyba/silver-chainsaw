import io
import json

from django.core import mail

from jsonschema import RefResolver, validate
from jsonschema.exceptions import ValidationError

DOCS_FILE = 'docs/openapi.json'


class MockResponse:
    """Utility class to mock http responses."""
    def __init__(self, status, data):
        self.status_code = status
        self.text = data

    def json(self):
        return self.text


def generate_image(**kwargs):
    """Generate image file.

    Based on FactoryBoy's ImageField (http://tiny.cc/zwmlsz)
    """
    from PIL import Image

    width = kwargs.get('width', 100)
    height = kwargs.get('height', width)
    color = kwargs.get('color', 'blue')
    image_format = kwargs.get('format', 'JPEG')
    image_palette = kwargs.get('palette', 'RGB')

    thumb_io = io.BytesIO()
    with Image.new(image_palette, (width, height), color) as thumb:
        thumb.save(thumb_io, format=image_format)
    return thumb_io


def get_latest_email():
    """Return latest email message sent."""
    assert len(mail.outbox) > 0
    return mail.outbox[-1]


def validate_schema(data, schema, debug=False):
    """Validate a given json data over a json schema.

    The schema has to belong to the documentation file: openapi.json
    """
    with open(DOCS_FILE, 'r') as fp:
        docs = json.load(fp)

    resolver = RefResolver('file:{}'.format(DOCS_FILE), docs)

    if debug:
        print('data:')
        print(data)
        print('schema:')
        print(docs['components']['schemas'][schema])

    try:
        validate(data, docs['components']['schemas'][schema], resolver=resolver)
    except ValidationError as e:
        # Work around difference between OpenAPI and JSON Schema.
        # The difference consists in the 'nullable' flag, which is not supported
        # in JSON Schema. Because of that, any validation error raised by None
        # values are ignored. See https://github.com/Julian/jsonschema/issues/533
        if not (e.instance is None and e.validator == 'type'):
            raise e
