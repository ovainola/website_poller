// Gruntfile for building coffee script
module.exports = function(grunt){
  grunt.initConfig({
    coffee: {
      compile: {
        options: {
          bare: true
        },
        files: [{
          expand: true,
          src: ['js/page_controller.coffee'],
          dest: 'templates',
          ext: '.js'
        }]
      }
    },
});


grunt.loadNpmTasks('grunt-contrib-coffee');

grunt.registerTask('build', ['coffee']);
grunt.registerTask('default', ['build']);
};
