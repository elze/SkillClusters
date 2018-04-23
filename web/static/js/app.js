/**
 * Created by Cherie Tabb on 8/30/2015.
 */
var app = angular.module('skillclusterApp', ['angularUtils.directives.dirPagination', 'ui.bootstrap']);

app.filter('unsafe', function($sce) {
    return function(val) {
        return $sce.trustAsHtml(val);
    };
  });

