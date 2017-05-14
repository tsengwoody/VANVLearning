class NormalEditor {
	constructor() {
		tinymce.init({
			selector: "#normalEditor",
			plugins: [
				'advlist autolink lists link image charmap print preview hr anchor pagebreak',
				'searchreplace wordcount visualblocks visualchars code fullscreen',
				'insertdatetime media nonbreaking save table contextmenu directionality',
				'emoticons template paste textcolor colorpicker textpattern imagetools codesample toc'
			],
			toolbar: 'undo redo | insert | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image | print preview media | forecolor backcolor emoticons | codesample',
		})
	}

	getEditorType = () => {
		return "normal";
	}

	getContent = () => {
		return tinymce.activeEditor.getContent();
	}

	resetContent = () => {
		tinymce.activeEditor.setContent('');
	}

	setContent = (html) => {
		tinymce.activeEditor.setContent(html);
	}
}

export default NormalEditor
