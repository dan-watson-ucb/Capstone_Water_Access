module.exports = {
    options: {
        jshintrc: '.jshintrc',
    },
    src: [
        '<%= config.src %>/**/*.js',
    ],
    tests: [
        '<%= config.tests %>/**/*.js'
    ],
    grunt: [
        'Gruntfile.js',
        '<%= config.grunt %>/**/*.js'
    ]
};
