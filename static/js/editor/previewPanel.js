class PreviewPanel {
	constructor(normalEditor, mathEditor) {
		this.container = document.getElementById('previewPanel');
		this.normalEditor = normalEditor;
		this.mathEditor = mathEditor;
		this.selectedEle = "";
	}

	setContent = () => {
		const type = $('.nav-tabs .active').text();
		const editor = (type === "normal")
			? this.normalEditor
			: this.mathEditor
		const html = editor.getContent();
		const newEle = document.createElement('div');

		if(this.selectedEle !== "") {
			if(this.selectedEle.className.split(' ')[0] === type) {
				this.selectedEle.innerHTML = html;
				editor.resetContent();
				this.selectedEle.className = this.selectedEle.className.split(' ')[0];
				this.selectedEle = "";
				return;
			}else {
				this.selectedEle.className = this.selectedEle.className.split(' ')[0];
				this.selectedEle = "";
			}
		}
		
		newEle.id = this.container.childElementCount + 1;
		newEle.className = type;
		newEle.innerHTML = html;
		newEle.addEventListener(
			"click",
			(type == 'normal')
			? this.handleContentToEditor(this.normalEditor)
			: this.handleContentToEditor(this.mathEditor)
		);
		
		this.container.appendChild(newEle);
		editor.resetContent();
	}
	
	handleContentToEditor = (editor) => (e) => {
		if(this.selectedEle !== "") {
			this.selectedEle.className = this.selectedEle.className.split(' ')[0];
		}
		const type = editor.getEditorType();

		let targetEle = e.target;
		while(targetEle.className !== type) {
			targetEle = targetEle.parentElement;
		}
		this.selectedEle = targetEle;
		this.selectedEle.className += ' selectedEle';

		editor.setContent(this.selectedEle.innerHTML);
		if(type === 'math') {
			$('.nav-tabs a[href="#mathEditorTab"]').tab('show');
		}else if(type === 'normal') {
			$('.nav-tabs a[href="#normalEditorTab"]').tab('show');
		}
	}

	moveUp = (e) => {
		e.stopPropagation();
		const position = this.selectedEle.id;
		if(position == 1) {
			console.log('This element is already at 1st position');
			return;
		}
		let previousEle = $('#previewPanel #' + String(Number(position) - Number(1)))[0];
		
		this.switchEle(previousEle, this.selectedEle, 'up');
	}

	moveDown = (e) => {
		e.stopPropagation();
		const position = this.selectedEle.id;
		if(position == this.container.childElementCount) {
			console.log('This element is already at last position');
			return;
		}
		
		let nextEle = $('#previewPanel #' + String(Number(position) + Number(1)))[0];

		this.switchEle(this.selectedEle, nextEle, 'down');
	}

	switchEle = (pre, next, direction) => {
		const temp = pre.innerHTML;
		pre.innerHTML = next.innerHTML;
		next.innerHTML = temp;
		if(direction == 'up') {
			this.removeSelected(next);
			this.addSelected(pre);
		}else if(direction == 'down') {
			this.removeSelected(pre);
			this.addSelected(next);
		}
	}

	removeSelected = (ele) => {
		ele.className = ele.className.split(' ')[0];
		this.selectedEle = "";
	}

	addSelected = (ele) => {
		ele.className += ' selectedEle';
		this.selectedEle = ele;
	}
}

export default PreviewPanel;
