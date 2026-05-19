# CLI-Task-Tracker

Tasker is a simple command-line application for tracking and managing tasks.

## Features

* Add tasks
* Delete tasks
* List tasks
* Filter tasks by status
* Mark tasks as:

  * NOT_STARTED
  * IN_PROGRESS
  * DONE

## Installation

Install with `uv`:

```bash
uv tool install git+https://github.com/<YOUR_GITHUB_USERNAME>/cli-task-tracker.git
```

After installation, the `tasker` command will be available globally.

## Development

Clone the repository:

```bash
git clone https://github.com/<YOUR_GITHUB_USERNAME>/cli-task-tracker.git
cd cli-task-tracker
```

Install dependencies:

```bash
uv sync
```

Run the application:

```bash
uv run tasker ls
```

## Usage

### Add tasks

```bash
tasker add "read a book"
```

```bash
tasker add "do this" "do that"
```

### List all tasks

```bash
tasker ls
```

### List tasks by status

```bash
tasker ls done
```

```bash
tasker ls in_progress
```

```bash
tasker ls not_started
```

### Mark task status

```bash
tasker mark-in-progress 1
```

```bash
tasker mark-done 1
```

```bash
tasker mark-not-started 1
```

### Delete tasks

```bash
tasker del 1
```

## License

MIT
