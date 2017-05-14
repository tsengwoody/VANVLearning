import MathEditor from './mathEditor';
import NormalEditor from './normalEditor';
import PreviewPanel from './previewPanel';



window.onload = () => {
	const mathEditor = new MathEditor();
	const normalEditor = new NormalEditor();
	const previewPanel = new PreviewPanel(normalEditor, mathEditor);

	document.getElementById('button_to_panel').addEventListener("click", previewPanel.setContent);
	document.getElementById('button_up').addEventListener("click", previewPanel.moveUp);
	document.getElementById('button_down').addEventListener("click", previewPanel.moveDown);
}
