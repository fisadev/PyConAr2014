require('es6-promise').polyfill();

var gulp          = require('gulp');
var sass          = require('gulp-sass');
var autoprefixer  = require('gulp-autoprefixer');
var rename        = require('gulp-rename');

var concat = require('gulp-concat');
var jshint = require('gulp-jshint');
var uglify = require('gulp-uglify');

var plumber = require('gulp-plumber');
var gutil   = require('gulp-util');

var browserSync = require('browser-sync').create();
var reload      = browserSync.reload;

var neat = require('node-neat').includePaths;

var onError = function (err) {
console.log('An error occurred:', gutil.colors.magenta(err.message));
gutil.beep();
this.emit('end');
};

gulp.task('vendor', function() {
return gulp.src([
		'./js/vendor/jquery-3.2.1.js'
	])
	.pipe(concat('vendor.js'))
	.pipe(rename({suffix: '.min'}))
	.pipe(uglify())
	.pipe(gulp.dest('./js'))
});

gulp.task('scripts', function() {
return gulp.src(['./js/app/*.js'])
	.pipe(jshint())
	.pipe(jshint.reporter('default'))
	.pipe(concat('app.js'))
	.pipe(rename({suffix: '.min'}))
	.pipe(uglify())
	.pipe(gulp.dest('./js'))
});

gulp.task('sass', function() {
return gulp.src('./scss/**/*.scss')
	.pipe(plumber({ errorHandler: onError }))
	.pipe(sass({
		includePaths: [neat]
	}))
	.pipe(gulp.dest('./css'));
});

gulp.task('watch', function() {

browserSync.init({
	open: false,
	server: true,
	files: ['./*.html']
});
gulp.watch('./scss/**/*.scss', ['sass', reload]);
gulp.watch('./js/vendor/*.js', ['vendor', reload]);
gulp.watch('./js/app/*.js', ['scripts', reload]);
});

gulp.task('default', ['sass', 'vendor', 'scripts', 'watch']);
gulp.task('build', ['sass', 'vendor', 'scripts']);
