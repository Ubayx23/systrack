// Terminal JavaScript for SysTrack Web App

class Terminal {
    constructor() {
        this.output = document.getElementById('output');
        this.input = document.getElementById('commandInput');
        this.commandHistory = [];
        this.historyIndex = -1;
        this.init();
    }

    init() {
        // Focus input on load
        this.input.focus();

        // Handle command submission
        this.input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                this.executeCommand();
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                this.navigateHistory(-1);
            } else if (e.key === 'ArrowDown') {
                e.preventDefault();
                this.navigateHistory(1);
            } else if (e.key === 'Tab') {
                e.preventDefault();
                // Could implement tab completion here
            }
        });

        // Keep input focused when clicking terminal
        document.getElementById('terminal').addEventListener('click', () => {
            this.input.focus();
        });

        // Auto-scroll to bottom
        this.scrollToBottom();
    }

    async executeCommand() {
        const command = this.input.value.trim();
        
        if (!command) {
            return;
        }

        // Add to history
        if (command !== this.commandHistory[this.commandHistory.length - 1]) {
            this.commandHistory.push(command);
        }
        this.historyIndex = this.commandHistory.length;

        // Display command
        this.addLine(`<span class="prompt">systrack@localhost:~$</span> ${command}`, 'command-output');

        // Clear input
        this.input.value = '';

        // Handle clear command locally
        if (command.toLowerCase() === 'clear' || command.toLowerCase() === 'cls') {
            this.clearTerminal();
            return;
        }

        // Show loading
        const loadingLine = this.addLine('Processing...', 'loading');

        try {
            // Send command to server
            const response = await fetch('/api/command', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ command: command })
            });

            const data = await response.json();

            // Remove loading
            loadingLine.remove();

            // Display result
            if (data.error) {
                this.addLine(`Error: ${data.error}`, 'command-error');
            } else if (data.output) {
                // Split output by lines and display
                const lines = data.output.split('\n');
                lines.forEach(line => {
                    if (line.trim()) {
                        this.addLine(line, 'command-output');
                    }
                });
            }
        } catch (error) {
            loadingLine.remove();
            this.addLine(`Error: ${error.message}`, 'command-error');
        }

        this.scrollToBottom();
    }

    addLine(text, className = '') {
        const line = document.createElement('div');
        line.className = `terminal-line ${className}`;
        line.innerHTML = text;
        this.output.appendChild(line);
        return line;
    }

    clearTerminal() {
        this.output.innerHTML = '';
        this.addLine('<span class="prompt">Terminal cleared</span>', 'command-success');
        this.scrollToBottom();
    }

    navigateHistory(direction) {
        if (this.commandHistory.length === 0) return;

        this.historyIndex += direction;

        if (this.historyIndex < 0) {
            this.historyIndex = 0;
        } else if (this.historyIndex >= this.commandHistory.length) {
            this.historyIndex = this.commandHistory.length;
            this.input.value = '';
            return;
        }

        this.input.value = this.commandHistory[this.historyIndex];
    }

    scrollToBottom() {
        this.output.parentElement.scrollTop = this.output.parentElement.scrollHeight;
    }
}

// Initialize terminal when page loads
document.addEventListener('DOMContentLoaded', () => {
    new Terminal();
});

