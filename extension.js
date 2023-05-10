const vscode = require('vscode');
const axios = require('axios');
const path = require('path');
const {getAssertLines} = require('./utils');


/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
	const decorationType = vscode.window.createTextEditorDecorationType({
		backgroundColor: 'rgba(255, 255, 0, 0.1)',
		isWholeLine: true
	  });

	const nullDecorationType = vscode.window.createTextEditorDecorationType({
		backgroundColor: new vscode.ThemeColor("editor.background"),
		gutterIconPath: path.join(__dirname, 'assert-gutter.svg'),
		isWholeLine: true
	});



	async function generateAsserts(level){
		let url;
		if (level === "naive"){
			url = 'http://127.0.0.1:5000/genNaiveAssert'
		}else if (level === "fewShot"){
			url = 'http://127.0.0.1:5000/genFewShotAssert'
		}

		let editor = vscode.window.activeTextEditor;
		if (!editor){
			vscode.window.showErrorMessage('No active editor found');
      		return;
		}
		const selection = editor.selection;
		let selectedText = editor.document.getText(selection);
		if (!selectedText) {
			vscode.window.showErrorMessage('No text selected');
			return;
		}

		let selectedRange = new vscode.Range(selection.start, selection.end);
		const originalFileUri = editor.document.uri;
    	const originalFileExt = path.extname(originalFileUri.fsPath);

		vscode.window.withProgress({
			location: vscode.ProgressLocation.Notification,
			title: 'Generating Assertions...',
			cancellable: false
		  }, () => {
			return new Promise(resolve => {
				// @ts-ignore
				axios.post(url, { code: selectedText, code_extension: originalFileExt})
				.then(response => {
					resolve();
					let responseCode = response.data;
					editor.edit((editBuilder) => {
						editBuilder.replace(selectedRange, responseCode);
					}).then(done => {
						let assertLineNumbers = getAssertLines(responseCode);
						console.log(assertLineNumbers);
						const decorations = assertLineNumbers.map(lineNumber => {
							const adjustedLineNumber = selectedRange.start.line + lineNumber;
							console.log("Line count : " + editor.document.lineCount);
							const line = editor.document.lineAt(adjustedLineNumber);
							return {
								range: new vscode.Range(line.range.start, line.range.end),
							}
						});
						editor.setDecorations(nullDecorationType,[]);
						editor.setDecorations(decorationType, decorations);
					})
					
				})
				.catch(error => {
					resolve();
					console.error(error);
					vscode.window.showErrorMessage('Some unexpected error occurred.');
				})
			})
		  });
	}

	let naiveDisposable = vscode.commands.registerCommand('assertron.generateNaiveAssert', generateAsserts.bind(null, "naive"));
	let fewShotDisposable = vscode.commands.registerCommand('assertron.generateFewShotAssert', generateAsserts.bind("null", "fewShot"));
	context.subscriptions.push(naiveDisposable, fewShotDisposable);

	const mergeButton = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left);
    mergeButton.text = "$(check) Merge Assertion";
	mergeButton.command = "assertron.mergeAssertion"
    mergeButton.show();

    const discardButton = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left);
    discardButton.text = "$(trashcan) Discard Assertion";
	discardButton.command = "assertron.discardAssertion"
    discardButton.show();

    context.subscriptions.push(mergeButton);
    context.subscriptions.push(discardButton);

	vscode.window.onDidChangeTextEditorSelection(event => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
			vscode.window.showErrorMessage('No active editor found');
      		return;
        }
        const selectedRange = editor.selection;
        if (selectedRange.isEmpty) {
            mergeButton.tooltip = "Select at least one assertion to merge";
            mergeButton.color = undefined;
            mergeButton.command = undefined;
            discardButton.tooltip = "Select at least one assertion to discard";
            discardButton.color = undefined;
            discardButton.command = undefined;
        } else {
			mergeButton.tooltip = "Merge Selected Assertions";
            mergeButton.color = "Green";
			mergeButton.backgroundColor =  new vscode.ThemeColor("editor.background");
            mergeButton.command = "assertron.mergeAssertion";
            discardButton.tooltip = "Discard Selected Assertions";
            discardButton.color = "Red";
            discardButton.command = "assertron.discardAssertion";
			discardButton.backgroundColor =  new vscode.ThemeColor("editor.background");
        }
    });

	let mergeAssertionDisposable = vscode.commands.registerCommand('assertron.mergeAssertion', () => {
		const editor = vscode.window.activeTextEditor;
		if (!editor){
			vscode.window.showErrorMessage('No active editor found');
      		return;
		}
		const selectedRange = editor.selection;
		let assertLineNumbers = getAssertLines(editor.document.getText(selectedRange));
		const decorations = assertLineNumbers.map(lineNumber => {
			const adjustedLineNumber = selectedRange.start.line + lineNumber;
			console.log(adjustedLineNumber);
			const line = editor.document.lineAt(adjustedLineNumber);
			return {
				range: new vscode.Range(line.range.start, line.range.end),
			}
		});
		editor.setDecorations(nullDecorationType, decorations);
		vscode.window.showInformationMessage('Assertions merged.');
	});

	let discardAssertionDisposable = vscode.commands.registerCommand('assertron.discardAssertion', () => {
		const editor = vscode.window.activeTextEditor;
		if (!editor){
			vscode.window.showErrorMessage('No active editor found');
      		return;
		}
		const selection = editor.selection;
		const document = editor.document;
		
		let edits = [];
		for (let i = selection.start.line; i <= selection.end.line; i++) {
			const line = document.lineAt(i);
			const lineText = line.text;
			if (!lineText.includes("assert")) {
				continue;
			}
			const range = new vscode.Range(line.range.start, line.range.end);
			const edit = new vscode.TextEdit(range, '');
			edits.push(edit);
		}	  
		const workspaceEdit = new vscode.WorkspaceEdit();
		workspaceEdit.set(document.uri, edits);
		vscode.workspace.applyEdit(workspaceEdit);
		vscode.window.showInformationMessage('Assertions discarded.');
	});

	context.subscriptions.push(mergeAssertionDisposable, discardAssertionDisposable);

}

function deactivate() {}

module.exports = {
	activate,
	deactivate
}
