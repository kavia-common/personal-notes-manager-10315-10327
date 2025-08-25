"""Notes routes exposing CRUD API using flask-smorest."""
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app.schemas.notes import NoteSchema, NoteCreateSchema, NoteUpdateSchema
from app.services.notes_service import notes_service

blp = Blueprint(
    "Notes",
    "notes",
    url_prefix="/api/notes",
    description="Operations for creating, reading, updating, and deleting notes",
)


@blp.route("/")
class NotesList(MethodView):
    """List and create notes."""

    @blp.response(200, NoteSchema(many=True))
    @blp.doc(summary="List notes", description="Return all notes sorted by last update time (desc).", tags=["Notes"])
    def get(self):
        """Get all notes."""
        return notes_service.list_notes()

    @blp.arguments(NoteCreateSchema)
    @blp.response(201, NoteSchema)
    @blp.doc(summary="Create note", description="Create a new note with title and content.", tags=["Notes"])
    def post(self, payload):
        """Create a note."""
        note = notes_service.create_note(title=payload["title"], content=payload["content"])
        return note, 201


@blp.route("/<int:note_id>")
class NotesDetail(MethodView):
    """Retrieve, update, and delete a single note by ID."""

    @blp.response(200, NoteSchema)
    @blp.doc(summary="Get note", description="Retrieve a note by its ID.", tags=["Notes"])
    def get(self, note_id: int):
        """Get a note by id."""
        note = notes_service.get_note(note_id)
        if not note:
            abort(404, message="Note not found")
        return note

    @blp.arguments(NoteUpdateSchema)
    @blp.response(200, NoteSchema)
    @blp.doc(
        summary="Update note",
        description="Update an existing note's title and/or content.",
        tags=["Notes"],
    )
    def put(self, payload, note_id: int):
        """Update a note by id."""
        if not payload:
            abort(400, message="No fields provided for update")
        updated = notes_service.update_note(note_id, title=payload.get("title"), content=payload.get("content"))
        if not updated:
            abort(404, message="Note not found")
        return updated

    @blp.response(204)
    @blp.doc(summary="Delete note", description="Delete a note by its ID.", tags=["Notes"])
    def delete(self, note_id: int):
        """Delete a note by id."""
        ok = notes_service.delete_note(note_id)
        if not ok:
            abort(404, message="Note not found")
        return "", 204
