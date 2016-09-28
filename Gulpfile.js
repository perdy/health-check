var gulp = require('gulp'),
  del = require('del'),
  sass = require('gulp-sass'),
  cssmin = require('gulp-minify-css'),
  browserify = require('browserify'),
  babelify = require('babelify'),
  uglify = require('gulp-uglify'),
  concat = require('gulp-concat'),
  rename = require('gulp-rename'),
  flatmap = require('gulp-flatmap'),
  eslint = require('gulp-eslint'),
  path = require('path'),
  source = require('vinyl-source-stream'),
  buffer = require('vinyl-buffer'),
  pkg = require('./package.json');

var gulpArgs = {
  cwd: path.join(process.cwd(), pkg.paths.static)
};

/**
 * Cleaning dist/ folder
 */
gulp.task('clean', function () {
  del.sync([pkg.dest.dist + '/**'], gulpArgs);
});

/**
 * Fonts
 */
gulp.task('fonts', function () {
  return gulp.src(pkg.paths.fonts)
    .pipe(gulp.dest(pkg.dest.fonts, gulpArgs))
});

/**
 * CSS
 */
gulp.task('css', function () {
  return gulp.src(pkg.paths.css)
    .pipe(cssmin())
    .pipe(gulp.dest(pkg.dest.css, gulpArgs))
});

/**
 * Scss compilation
 */
var sassOptions = {
  errLogToConsole: true,
  outputStyle: 'expanded',
  includePaths: ['./node_modules']
};
gulp.task('styles', function () {
  return gulp.src(pkg.paths.scss, gulpArgs)
    .pipe(sass(sassOptions).on('error', sass.logError))
    .pipe(concat(pkg.dest.style))
    .pipe(gulp.dest(pkg.dest.dist, gulpArgs));
});
gulp.task('styles:min', function () {
  return gulp.src(pkg.paths.scss, gulpArgs)
    .pipe(sass(sassOptions).on('error', sass.logError))
    .pipe(concat(pkg.dest.style))
    .pipe(cssmin())
    .pipe(gulp.dest(pkg.dest.dist, gulpArgs));
});

/**
 * JSLint/JSHint validation
 */
var eslintOptions = {
  baseConfig: {
    parserOptions: {
      "ecmaVersion": 6,
      "sourceType": "module",
      "ecmaFeatures": {
        "jsx": true
      }
    }
  }
};
gulp.task('lint', function () {
  return gulp.src([pkg.paths.js, pkg.paths.jsx], gulpArgs)
    .pipe(eslint(eslintOptions))
    .pipe(eslint.format())
    .pipe(eslint.failAfterError());
});

/** JavaScript compilation */
gulp.task('js', function () {
  return gulp.src(pkg.paths.apps, gulpArgs)
    .pipe(flatmap(function (stream, file) {
      return browserify(file.path)
        .transform(babelify, {presets: ["es2015", "react"]})
        .bundle()
        .pipe(source(file.path))
        .pipe(rename({dirname: pkg.dest.apps, extname: '.js'}))
        .pipe(gulp.dest(pkg.dest.dist, gulpArgs));
    }));
});
gulp.task('js:min', function () {
  process.env.NODE_ENV = 'production';
  return gulp.src(pkg.paths.apps, gulpArgs)
    .pipe(flatmap(function (stream, file) {
      return browserify(file.path)
        .transform(babelify, {presets: ["es2015", "react"]})
        .bundle()
        .pipe(source(file.path))
        .pipe(rename({dirname: pkg.dest.apps, extname: '.js'}))
        .pipe(buffer())
        .pipe(uglify())
        .pipe(gulp.dest(pkg.dest.dist, gulpArgs));
    }));
});

/**
 * Compiling resources and serving application
 */
gulp.task('default:watch', function () {
  gulp.watch(
    [pkg.paths.js, pkg.paths.jsx]
      .map(function (obj) { return path.join(pkg.paths.static, obj)}),
    ['lint', 'js'],
    gulpArgs
  );
  gulp.watch(
    [pkg.paths.scss]
      .map(function (obj) { return path.join(pkg.paths.static, obj)}),
    ['styles']
  );
});
gulp.task('default', ['clean', 'fonts', 'css', 'lint', 'styles', 'js', 'default:watch']);

gulp.task('dist:watch', function () {
  gulp.watch(
    [pkg.paths.js, pkg.paths.jsx]
      .map(function (obj) { return path.join(pkg.paths.static, obj)}),
    ['lint', 'js:min'],
    gulpArgs
  );
  gulp.watch(
    [pkg.paths.scss]
      .map(function (obj) { return path.join(pkg.paths.static, obj)}),
    ['styles:min']
  );
});
gulp.task('dist', ['clean', 'fonts', 'css', 'lint', 'styles:min', 'js:min']);
