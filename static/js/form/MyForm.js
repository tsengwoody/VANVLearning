import React, { PropTypes, Component } from 'react';
import { Row, Col, Form, Select, Radio, Input } from 'antd';
const FormItem = Form.Item;
const Option = Select.Option;
const RadioGroup = Radio.Group;

class MyForm extends Component {
	constructor(props) {
		super();
	}

	render() {
		console.log(this.props.formData);
		const { getFieldDecorator } = this.props.form;
		const formItemLayout = {
			labelCol: { span: 1 },
			wrapperCol: { span: 10 },
		};

		const formTypeRouter = (formData) => {
			if(!formData) return null;
			const formDataAry = Object.values(formData);
			const length = formDataAry.length;
			return formDataAry.map(data => {
				if(data.type === "Select") {
					return genSelect(data);
				}else if(data.type === "RadioSelect") {
					return genRadio(data);
				}else if(data.type === "Textarea") {
					return genTextArea(data);
				}else {
					console.warn("There is no type matched with form data");
				}
			})
		}
			
		const genSelect = (config) => {
			if(!config) return null;
			return (
				<FormItem label={config.label} {...formItemLayout}>
					{getFieldDecorator(config.name)(
						<Select>
							{config.choices.map((choice, index) => <Option key={choice+index} value={String(index)}>{choice}</Option>)}
						</Select>
					)}
				</FormItem>
			)
		}

		const genRadio = (config) => {
			if(!config) return null;
			return (
				<FormItem label={config.label} {...formItemLayout}>
					{getFieldDecorator(config.name)(
						<RadioGroup>
							{config.choices.map((choice, index) => <Radio key={choice} value={choice[0]}>{choice[1]}</Radio>)}
						</RadioGroup>
					)}
				</FormItem>
			);
		}

		const genTextArea = (config) => {
			if(!config) return null;
			return (
				<FormItem label={config.label} {...formItemLayout}>
					{getFieldDecorator(config.name)(
						<Input type="textarea" autosize={{minRows: 10}}></Input>
					)}
				</FormItem>
			);
		}

		return (
			<Form>
				{ formTypeRouter(this.props.formData) }
				{/*
				{ genSelect(this.props.formData[0]) }
				{ genSelect(this.props.formData[1]) }
				{ genRadio(this.props.formData[2]) }
				{ genTextArea(this.props.formData[3]) }
				{ genTextArea(this.props.formData[4]) }
				*/}
			</Form>
		)
	}
}

MyForm.propTypes = {
	formData:	PropTypes.object.isRequired,
}

const WrapperMyForm = Form.create()(MyForm);

export default WrapperMyForm;
