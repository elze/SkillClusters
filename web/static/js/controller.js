/**
 * Created by Cherie Tabb on 8/30/2015.
 */
app.controller('MainController', ['$scope', '$http', function ($scope, $http) {
    $scope.title = 'Welcome to SkillClusters!';
    $scope.showAssociatedSkills = [];
    $scope.secondarySkillStyle = [];
    $scope.ratiosToDisplay = [];

    secondaryBoxColors = ['#D6FFEB', '#C2FFE0', '#ADFFD6', '#99FFCC', '#7ACCA3', '#5C997A', '#3D6652'];

    $http.get('http://127.0.0.1:5000/skills')
        .then(function (result) {
            $scope.skills = result.data;
            $scope.skills_length = result.data.length;
            for (var i = 0; i < $scope.skills_length; i++) {
                $scope.showAssociatedSkills[i] = false;
                var skill = $scope.skills[i];
                $scope.secondarySkillStyle[i] = [];
		$scope.ratiosToDisplay[i] = [];
                for (var j = 0; j < skill.associated_terms.length; j++) {
		  var width = skill.associated_terms[j].ratio * 7000;
		  var sqRootWidth = Math.floor(Math.sqrt(width));
		  var computedSide = width;
		  if (sqRootWidth > 100) {
		    computedSide = sqRootWidth;
		  }
		  //var remainderWidth = width;
		  var remainderWidth = computedSide;
		  var previousRemainderWidth = remainderWidth;
		  var height = 30;
		  var padding = 0;
		  var fontSize = 100;
		  var fontSizeFactor = 1;
		  var paddingIncrease = 0;
		  var padding = 0;
		  var wordBreak = 'normal';
		  var boxColor = '#D6FFEB';
		  var ratioToDisplay;
		  if (skill.associated_terms[j].ratio < 0.01) {
		    //ratioToDisplay = "< 0.01";
		    $scope.ratiosToDisplay[i][j] = "< 0.01";
		  }
		  else {
		    //ratioToDisplay = skill.associated_terms[j].ratio.toFixed(2);
		    var ratioFloat = Number.parseFloat(skill.associated_terms[j].ratio);
		    //$scope.ratiosToDisplay[i][j] = skill.associated_terms[j].ratio.toFixed(2);
		    $scope.ratiosToDisplay[i][j] = ratioFloat.toFixed(2);
		  }

		  var fontScaleFactor = 1;
		  /*********
		  while (remainderWidth > 300) {
		    previousRemainderWidth = remainderWidth;
		    remainderWidth = remainderWidth - 300;
		    height = height + 1;
		    paddingIncrease = paddingIncrease + 2;
		    //padding = "30% 0%";		    
		    fontSizeFactor = fontSizeFactor + 1;
		  }
		  **********/
		  if (computedSide > 200) {
		    var boxSizeFactor = computedSide / 200;
		    var colorIndex = Math.floor(boxSizeFactor / 2);
		    if (colorIndex > secondaryBoxColors.length - 1) {
		      //console.log("colorIndex = " + colorIndex + " larger than secondaryBoxColors.length - 1");
		      colorIndex = secondaryBoxColors.length - 1;
		    }
		    boxColor = secondaryBoxColors[colorIndex];
		    var boxScaleFactor = 0.02 * boxSizeFactor;
		    var fontScaleFactor = 1 + 0.1 * boxSizeFactor;
		    computedSide = Math.floor(200 + 100 * boxScaleFactor);
		    paddingIncrease = Math.floor(boxSizeFactor * 1.05);
		    wordBreak = 'break-all';
		  }

		  previousRemainderWidth = previousRemainderWidth + "px";
		  height = height + "px";
		  fontSize = Math.floor(fontScaleFactor * 100) + "%";
		  padding = paddingIncrease + "% 0%";
		  //padding = paddingIncrease + "% 0%";
		  computedSide = computedSide + "px";
		    
		  
		  //$scope.secondarySkillStyle[i][j] = {'width': previousRemainderWidth, 'height': height, 'background-color': '#C2FFC2', 'margin':'5px 0px', 'padding': padding, 'text-align': 'center', 'fontSize': fontSize };
		  //$scope.secondarySkillStyle[i][j] = {'width': computedSide, 'height': computedSide, 'background-color': '#C2FFC2', 'margin':'5px 0px', 'padding': padding, 'text-align': 'center', 'fontSize': fontSize, 'word-break': wordBreak };
		  $scope.secondarySkillStyle[i][j] = {'width': computedSide, 'height': computedSide, 'background-color': boxColor, 'margin':'5px 0px', 'text-align': 'center', 'fontSize': fontSize, 'word-break': wordBreak };
                }
            }

        });
    $scope.setShowAssociatedSkills = function (i) {
        $scope.showAssociatedSkills[i] = !$scope.showAssociatedSkills[i];
    }
}]);
