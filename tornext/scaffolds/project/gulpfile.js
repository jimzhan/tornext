var pkg     = 'app';
//##################
// Gulp tools set  #
//##################
var gulp    = require('gulp');
var coffee  = require('gulp-coffee');
var concat  = require('gulp-concat');
var minify  = require('gulp-minify-css');
var rename  = require('gulp-rename');
var run     = require('gulp-run');
var sass    = require('gulp-sass');
var uglify  = require('gulp-uglify');
var util    = require('gulp-util');
var watch   = require('gulp-watch');

var md5     = require('md5');
var remove  = require('del');
var exec    = require('child_process').exec;

//############
// Constants #
//############
var paths = {
    assets:     './assets/'
};

var build = {
    python:     './**/*.pyc',
    styles:     './assets/**/*.css',
    scripts:    './assets/**/*.js',
};

var src = {
    python:     './apps/**/*.py',
    scripts:    './assets/scripts/**/*.coffee',
    styles:     './assets/styles/**/*.scss',
    templates:  './templates/**/*.html'
};

//#############
// Gulp Tasks #
//#############
gulp.task('build', function() {
    // compile & concat coffee scripts
    gulp.src(src.scripts)
        .pipe(coffee())
        .pipe(concat(pkg + '.js'))
        .pipe(rename({suffix: '.min'}))
        .pipe(uglify())
        .pipe(gulp.dest(paths.assets));
    // compile & concat scss
    gulp.src(src.styles)
        .pipe(sass())
        .pipe(concat(pkg + '.css'))
        .pipe(rename({suffix: '.min'}))
        .pipe(minify())
        .pipe(gulp.dest(paths.assets));
});

gulp.task('clean', function() {
    remove([build.python, build.styles, build.scripts], function(error) {
        if (error) console.log('Error: ' + error);
    });
});

gulp.task('rebuild', function() {
    gulp.start('clean');
    gulp.start('build');
});

var app = { server: {}, debug: true, port: 8000 };
gulp.task('serve', function(callback) {
    app.server = exec('python app.py --debug=' + app.debug + ' --port=' + app.port);
    app.server.stdout.pipe(process.stdout);
    app.server.stderr.pipe(process.stderr);
    util.log('Tornado server started (Port: ' + app.port + ')');
});

gulp.task('watch', function() {
    gulp.start('build');
    gulp.watch([src.scripts, src.styles, src.templates], function() {
        gulp.start('rebuild');
    });
});

gulp.task('default', ['watch', 'serve']);
