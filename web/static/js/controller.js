/**
 * Created by Cherie Tabb on 8/30/2015.
 */
app.controller('MainController', ['$scope', '$http', function ($scope, $http) {
    $scope.title = 'Welcome to SkillClusters!';

    $http.get('http://127.0.0.1:5000/skills')
        .then(function (result) {
            $scope.skills = result.data;

        });
    $scope.setShowAssociatedSkills = function() {
        $scope.showAssociatedSkills = true;
    }
}]);
