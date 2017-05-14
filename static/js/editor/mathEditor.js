class MathEditor {
	constructor() {
		this.editor = com.wiris.jsEditor.JsEditor.newInstance({'language': 'en'});
		this.editor.insertInto(document.getElementById('mathEditor'));
	}

	getEditorType = () => {
		return "math";
	}

	getContent = () => {
		return this.editor.getMathML();
	} 
	
	resetContent = () => {
		this.editor.setMathML("<math></math>");
	}

	setContent = (html) => {
		this.editor.setMathML(html);
	}
}

export default MathEditor;
