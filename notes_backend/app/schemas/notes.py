"""Marshmallow schemas for Notes API."""
from marshmallow import Schema, fields, validate


class NoteSchema(Schema):
    """Represents a Note entity."""
    id = fields.Int(required=True, description="Unique note identifier")
    title = fields.Str(required=True, validate=validate.Length(min=1, max=256), description="Note title")
    content = fields.Str(required=True, description="Note content")
    created_at = fields.Float(required=True, description="Creation timestamp (epoch seconds)")
    updated_at = fields.Float(required=True, description="Last update timestamp (epoch seconds)")


class NoteCreateSchema(Schema):
    """Payload for creating a note."""
    title = fields.Str(required=True, validate=validate.Length(min=1, max=256), description="Note title")
    content = fields.Str(required=True, description="Note content")


class NoteUpdateSchema(Schema):
    """Payload for updating a note. At least one of title or content must be provided."""
    title = fields.Str(required=False, validate=validate.Length(min=1, max=256), description="Note title")
    content = fields.Str(required=False, description="Note content")
