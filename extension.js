const vscode = require('vscode');
const axios = require('axios');
const path = require('path');

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
	let editor;
	let selectedRange;
	let selectedText;
	let responseData;
	let responseView;

	function closeWebView(){
		responseView.dispose();
	}

	function replaceCode(){
		editor.edit((editBuilder) => {
			editBuilder.replace(selectedRange, responseData);
		});
	}

	function getDiffLines(oldCode, newCode){
		const oldLines = oldCode.split('\n');
		const newLines = newCode.split('\n');
		let inds = [];
		for (let i=0; i<newLines.length; i++){
			const newLine = newLines[i];
			if (oldLines.includes(newLine)){
				inds.push(i);
				console.log(newLine);
			}
		}
		return inds;
	}
	
	async function generateNaiveAssertion() {
		editor = vscode.window.activeTextEditor;
		if (!editor){
			vscode.window.showErrorMessage('No active editor found');
      		return;
		}

		const selection = editor.selection;
		selectedText = editor.document.getText(selection);
		if (!selectedText) {
			vscode.window.showErrorMessage('No text selected');
			return;
		}

		selectedRange = new vscode.Range(selection.start, selection.end);
		const originalFileUri = editor.document.uri;
    	const originalFileExt = path.extname(originalFileUri.fsPath);
		
		vscode.window.withProgress({
			location: vscode.ProgressLocation.Notification,
			title: 'Generating Assertions...',
			cancellable: false
		  }, () => {
			return new Promise(resolve => {
				// @ts-ignore
				axios.post('http://127.0.0.1:5000/genNaiveAssert', { code: selectedText, code_extension: originalFileExt})
				.then(response => {
					resolve();
					responseData = response.data;
					const diffInds = getDiffLines(selectedText, responseData);
					console.log(diffInds);
					const viewType = 'responseView';
					const viewTitle = 'Generated Assertions';
					responseView = vscode.window.createWebviewPanel(viewType, viewTitle, vscode.ViewColumn.Two, {enableScripts: true});
					responseView.webview.onDidReceiveMessage(message => {
						if (message.command === 'discard') {

						} else if (message.command === 'merge') {

						}
						else if (message.command === 'close') {
							closeWebView();
						}
					});
					
					const vscodeStylesheetPath = vscode.Uri.file(
						'/Applications/Visual Studio Code.app/Contents/Resources/app/out/vs/workbench/workbench.desktop.main.css'
					).with({ scheme: 'vscode-resource' });
					responseView.webview.html = `
					<!DOCTYPE html>
						<head>
							<link href="${vscodeStylesheetPath}" rel="stylesheet">
							<style>
								body {
									background-color: var(--vscode-editor-background);
									color: var(--vscode-editor-foreground);
									font-family: var(--vscode-editor-font-family);
									font-size: var(--vscode-editor-font-size);
									line-height: var(--vscode-editor-line-height);
									padding: 20px;
									height: 100%;
									overflow: hidden;
								}
								h1 {
									margin-top: 0;
								}
							</style>		
						</head>
						<body>
							<div>
								<div>
									<h1><pre>${responseData}</pre></h1>
								</div>
							</div>
							<script>
								const vscode = acquireVsCodeApi();
								const closeButton = document.getElementById('closeBtn');
								closeButton.addEventListener('click', () => {
									vscode.postMessage({
										command: 'close'
									});
								});
							</script>
						</body>
					</html>
				`;
				})
				.catch(error => {
					console.error(error);
					resolve();
					vscode.window.showErrorMessage('Some unexpected error occurred.');
				});
			})
		})

	}

	async function generateFewShotAssertion() {
		editor = vscode.window.activeTextEditor;
		if (!editor){
			vscode.window.showErrorMessage('No active editor found');
      		return;
		}

		const selection = editor.selection;
		selectedText = editor.document.getText(selection);
		if (!selectedText) {
			vscode.window.showErrorMessage('No text selected');
			return;
		}

		selectedRange = new vscode.Range(selection.start, selection.end);
		const originalFileUri = editor.document.uri;
    	const originalFileExt = path.extname(originalFileUri.fsPath);
		
		vscode.window.withProgress({
			location: vscode.ProgressLocation.Notification,
			title: 'Generating Assertions...',
			cancellable: false
		  }, () => {
			return new Promise(resolve => {
				// @ts-ignore
				axios.post('http://127.0.0.1:5000/genFewShotAssert', { code: selectedText, code_extension: originalFileExt})
				.then(response => {
					resolve();
					responseData = response.data;
					const diffInds = getDiffLines(selectedText, responseData);
					console.log(diffInds);
					const viewType = 'responseView';
					const viewTitle = 'Generated Assertions';
					responseView = vscode.window.createWebviewPanel(viewType, viewTitle, vscode.ViewColumn.Two, {enableScripts: true});
					responseView.webview.onDidReceiveMessage(message => {
						if (message.command === 'discard') {

						} else if (message.command === 'merge') {

						}
						else if (message.command === 'close') {
							closeWebView();
						}
					});
					
					const vscodeStylesheetPath = vscode.Uri.file(
						'/Applications/Visual Studio Code.app/Contents/Resources/app/out/vs/workbench/workbench.desktop.main.css'
					).with({ scheme: 'vscode-resource' });
					responseView.webview.html = `
					<!DOCTYPE html>
						<head>
							<link href="${vscodeStylesheetPath}" rel="stylesheet">
							<style>
								body {
									background-color: var(--vscode-editor-background);
									color: var(--vscode-editor-foreground);
									font-family: var(--vscode-editor-font-family);
									font-size: var(--vscode-editor-font-size);
									line-height: var(--vscode-editor-line-height);
									padding: 20px;
									height: 100%;
									overflow: hidden;
								}
								h1 {
									margin-top: 0;
								}
							</style>		
						</head>
						<body>
							<div>
								<div>
									<h1><pre>${responseData}</pre></h1>
								</div>
							</div>
							<script>
								const vscode = acquireVsCodeApi();
								const closeButton = document.getElementById('closeBtn');
								closeButton.addEventListener('click', () => {
									vscode.postMessage({
										command: 'close'
									});
								});
							</script>
						</body>
					</html>
				`;
				})
				.catch(error => {
					console.error(error);
					resolve();
					vscode.window.showErrorMessage('Some unexpected error occurred.');
				});
			})
		})

	}

	const disposable = vscode.commands.registerCommand('assertron.generateNaiveAssert', generateNaiveAssertion);
	const fewShotdisposable = vscode.commands.registerCommand('assertron.generateFewShotAssert', generateFewShotAssertion);
	context.subscriptions.push(disposable);
	context.subscriptions.push(fewShotdisposable);
}

function deactivate() {}

module.exports = {
	activate,
	deactivate
}
