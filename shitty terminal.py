import subprocess
import os
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def index():
    return r"""<!DOCTYPE html>
<html>
<head>
    <title>Web Terminal</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
</head>
<body>
    <h1>Web Terminal</h1>
    <div id="terminal-output"></div>
    <form id="terminal-form">
        <input id="terminal-input" type="text" autofocus autocomplete="off" />
    </form>

    <script>
        $(document).ready(function() {
            var form = $('#terminal-form');
            var input = $('#terminal-input');
            var output = $('#terminal-output');

            form.submit(function(e) {
                e.preventDefault();
                var command = input.val().trim();
                input.val('');

                if (command === 'exit') {
                    output.append('<p>Goodbye!</p>');
                    return;
                }

                $.ajax({
                    type: 'POST',
                    url: '/execute_command',
                    data: { command: command },
                    success: function(response) {
                        output.append('<p>' + response + '</p>');
                    },
                    error: function(xhr, status, error) {
                        output.append('<p>Error: ' + error + '</p>');
                    }
                });
            });
        });
    </script>
</body>
</html>"""

@app.route('/execute_command', methods=['POST'])
def execute_command():
    command = request.form['command']
    command_parts = command.split()

    if command_parts[0] == 'cd':
        if len(command_parts) == 1:
            current_dir = os.getcwd()
            return f"Current directory: {current_dir}"
        else:
            try:
                os.chdir(command_parts[1])
                current_dir = os.getcwd()
                return f"Changed directory to: {current_dir}"
            except:
                return "Failed to change directory"
    elif command_parts[0] == 'cls':
        # Reload the page to clear the screen
        return "<script>location.reload();</script>"
    else:
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
            return output
        except subprocess.CalledProcessError as e:
            return str(e.output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000)