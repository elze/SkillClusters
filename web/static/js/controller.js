/**
 * Created by Cherie Tabb on 8/30/2015.
 */

app.directive('a', function() {
    return {
        restrict: 'E',
        link: function(scope, elem, attrs) {
            if(attrs.ngClick || attrs.href === '' || attrs.href === '#'){
                elem.on('click', function(e){
                    e.preventDefault();
                });
            }
        }
   };
});

app.controller('MainController', ['$scope', '$http', function ($scope, $http) {
    $scope.title = 'Welcome to SkillClusters!';
    $scope.showAssociatedSkills = [];
    $scope.secondarySkillStyle = [];
    $scope.ratiosToDisplay = [];

    //secondaryBoxColors = ['#D6FFEB', '#C2FFE0', '#ADFFD6', '#99FFCC', '#7ACCA3', '#5C997A', '#3D6652'];
    secondaryBoxColors = ['#BCD6C9', '#61B58D', '#7DB19B', '#AD6798', '#5E6B64', '#5B829C', '#2A1768'];

    $scope.primarySkillsPerPage = 5; // this should match however many results your API puts on one page
    var zeroBasedCurrentPage = 0;

    $http.get('http://127.0.0.1:5000/primary_skills_count')
        .then(function (result) {
	    $scope.primarySkillsCount = result.data.Count;
	    $scope.numberOfPages = Math.floor($scope.primarySkillsCount / $scope.primarySkillsPerPage);
	    if ($scope.primarySkillsCount % $scope.primarySkillsPerPage != 0) {
	      $scope.numberOfPages++;
	    }

	    $scope.pageNumbers = [];
	    for (var pageIndex = 0; pageIndex < $scope.numberOfPages; pageIndex++) {
	      $scope.pageNumbers[pageIndex] = pageIndex + 1;
	    }

	  });


    getResultsPage(1);
  
    $scope.pagination = {
    current: 1
    };

    $scope.pageChanged = function(newPage) {
      console.log('Skills page changed to ' + newPage);
      /***
	  for (var key in $scope.checkboxModels) {
	  console.log("pageChanged: deleting key = " + key);
	  delete $scope.checkboxModels[key];
	  }
      ********/
      getResultsPage(newPage);
      zeroBasedCurrentPage = newPage-1;
  };

  function getResultsPage(pageNumber) {
    $http.get('http://127.0.0.1:5000/skills/' + pageNumber + '/' + $scope.primarySkillsPerPage)
        .then(function (result) {
            $scope.skills = result.data;
            $scope.skills_length = result.data.length;
            for (var i = 0; i < $scope.skills_length; i++) {
                $scope.showAssociatedSkills[i] = false;
                var skill = $scope.skills[i];
                $scope.secondarySkillStyle[i] = [];
		$scope.ratiosToDisplay[i] = [];
                for (var j = 0; j < skill.associated_terms.length; j++) {
		  var computedSideX = 150;
		  var computedSideY = 50;
		  var fontSize = 100;
		  var fontSizeFactor = 1;
		  //var paddingIncrease = 0;
		  //var padding = 0;
		  //var wordBreak = 'normal';
		  //var boxColor = '#D6FFEB';
		  var ratio = skill.associated_terms[j].ratio;
		  if (skill.associated_terms[j].ratio < 0.01) {
		    $scope.ratiosToDisplay[i][j] = "< 0.01";
		  }
		  else {
		    var ratioAsNumber = Number.parseFloat(ratio);
		    $scope.ratiosToDisplay[i][j] = ratioAsNumber.toFixed(2);
		  }

		  var fontScaleFactor = 1;
		  var colorIndex = 0;
		  var boxScaleFactorX = 1;
		  var boxScaleFactorY = 1;
		  var fontScaleFactor = 1;

		    var percentage = ratio * 100;
		    var wholePercentage = Math.floor(percentage / 10);
		    var wholePercentageHalf = Math.floor(wholePercentage / 2);
		    boxScaleFactorX = 1 + 0.1 * wholePercentage;
		    boxScaleFactorY = 1 + 0.1 * wholePercentageHalf;
		    fontScaleFactor = 1 + 0.1 * wholePercentageHalf;
		    colorIndex = wholePercentageHalf;
		    var boxColor = secondaryBoxColors[colorIndex];
		    computedSideX = Math.floor(computedSideX * boxScaleFactorX);
		    computedSideY = Math.floor(computedSideY * boxScaleFactorX);

		    var wordBreak = 'break-all';

		  fontSize = Math.floor(fontScaleFactor * 100) + "%";
		  computedSideX = computedSideX + "px";
		  computedSideY = computedSideY + "px";
		    		  
		  //$scope.secondarySkillStyle[i][j] = {'width': computedSide, 'height': computedSide, 'background-color': '#C2FFC2', 'margin':'5px 0px', 'padding': padding, 'text-align': 'center', 'fontSize': fontSize, 'word-break': wordBreak };
		  $scope.secondarySkillStyle[i][j] = {'width': computedSideX, 'height': computedSideY, 'background-color': boxColor, 'margin':'5px 0px', 'text-align': 'center', 'fontSize': fontSize, 'word-break': wordBreak };
                }
            }

        });
  };

  $scope.searchByTerm = function(searchTerm) {
      console.log('searchByTerm: searchTerm = ' + searchTerm);
      /***
	  for (var key in $scope.checkboxModels) {
	  console.log("pageChanged: deleting key = " + key);
	  delete $scope.checkboxModels[key];
	  }
      ********/
      getResultsPage(newPage);
      zeroBasedCurrentPage = newPage-1;
  };


  $scope.setShowAssociatedSkills = function (i) {
    $scope.showAssociatedSkills[i] = !$scope.showAssociatedSkills[i];
  }

}]);
