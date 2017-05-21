module.exports = {
	entry: [
		'./static/js/form/index.js',
	],
	output: {
		path: `${__dirname}/static/js/bundle`,
		filename: 'form.js',
	},
	module: {
		loaders: [
			{	test: /\.js$/,
				exclude: /node_modules/,
				loader: 'babel-loader',
				presets: ['es2015', 'react', 'stage-0'],
			},
			{
				test: /\.css$/,
				loader: 'style-loader!css-loader',
			},
		],
	},
};
