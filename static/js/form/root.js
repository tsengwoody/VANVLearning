import React from 'react';
import MyForm from './MyForm';

import { Row, Col, Select, Button, Radio } from 'antd';
const Option = Select.Option;

class Root extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			formType: ['TextForm', 'TrueFalseForm', 'ChoiceForm', 'DescriptionForm'],
			formData: {}
		}
	}

	componentWillMount() {
		this.handleFetchFormData(this.state.formType[0]);
	}

	handleTransformValue = (v) => {
		this.handleFetchFormData(v.target.value);
	}

	handleFetchFormData = (v) => {
		$.ajax({
			url: '/MaterialADocument/get_form_info/' + v,
		})
		.done(function(data) {
			this.setState({
				formData: data
			})
		}.bind(this))
	}

	render() {
		const formTypeOptions = () => (
			this.state.formType.map(type => <Option key={type} value={type}>{type}</Option>)
		)

		const formTypeButtons = () => (
			<Radio.Group defaultValue={this.state.formType[0]} onChange={this.handleTransformValue}>
				<Radio.Button value={this.state.formType[0]}>課文</Radio.Button>
				<Radio.Button value={this.state.formType[1]}>是非題</Radio.Button>
				<Radio.Button value={this.state.formType[2]}>選擇題</Radio.Button>
				<Radio.Button value={this.state.formType[3]}>問答題</Radio.Button>
			</Radio.Group>
		)

		return (
			<div>
				<Row style={{marginBottom: 30}}>
					<Col offset={1} span={10}>
						{ formTypeButtons() }
					</Col>
				</Row>
				<Row>
					<MyForm formData={this.state.formData} />
				</Row>
			</div>
		);
	}
}

export default Root;
