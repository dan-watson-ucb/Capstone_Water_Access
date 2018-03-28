module.exports = {
    options: {
        config: '.jscsrc'
    },
    src: {
        src: [
            '<%= config.src %>/**/*.js',
        ]
    },
    tests: {
        src: '<%= config.tests %>/**/*.js'
    },
    grunt: {
        src: [
            'Gruntfile.js',
            '<%= config.grunt %>/**/*.js'
        ]
    }
};
