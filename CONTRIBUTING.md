# Contributing to LLM Eval & Tracing Infrastructure

First off, thank you for considering contributing to this project!

## Development Setup

1. **Fork and clone the repository.**
2. **Install dependencies:**
   ```bash
   make install
   ```
3. **Run the backend:**
   ```bash
   make start-backend
   ```
4. **Run the frontend:**
   ```bash
   cd frontend && npm run dev
   ```

## Workflow

- Create a new branch for your feature or bugfix.
- Ensure all tests pass: `make test`.
- Add documentation for new features.
- Submit a Pull Request with a clear description of the changes.

## Code Style

- Use Python type hints.
- Follow PEP 8 for Python and Prettier for TypeScript.
- Write descriptive commit messages.

## Commit History Suggestions

When submitting, try to keep a clean commit history. Recommended structure:
- `feat: add universal trace collector`
- `fix: resolve race condition in Redis queue`
- `docs: update README with architecture diagram`
- `test: add integration tests for evaluation engine`

## Questions?

Feel free to open an issue or contact the maintainers.
