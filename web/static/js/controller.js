/**
 * Created by Cherie Tabb on 8/30/2015.
 */
app.controller('MainController', ['$scope', '$http', function ($scope, $http) {
    $scope.title = 'Welcome to SkillClusters!';
    $scope.showAssociatedSkills = [];
    $scope.secondarySkillStyle = [];

    $http.get('http://127.0.0.1:5000/skills')
        .then(function (result) {
            $scope.skills = result.data;
            $scope.skills_length = result.data.length;
            for (var i = 0; i < $scope.skills_length; i++) {
                $scope.showAssociatedSkills[i] = false;
                var skill = $scope.skills[i];
                $scope.secondarySkillStyle[i] = [];
                for (var j = 0; j < skill.associated_terms.length; j++) {
                    var width = skill.associated_terms[j].ratio * 1000;
                    $scope.secondarySkillStyle[i][j] = "width: " + width + "px; color: #C2FFC2;";
                }
            }

        });
    $scope.setShowAssociatedSkills = function (i) {
        $scope.showAssociatedSkills[i] = !$scope.showAssociatedSkills[i];
    }
}]);
