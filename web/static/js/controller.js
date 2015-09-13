/**
 * Created by Cherie Tabb on 8/30/2015.
 */
app.controller('MainController', ['$scope', '$http', function ($scope, $http) {
    $scope.title = 'Welcome to SkillClusters!';
    $scope.showAssociatedSkills = [];
    $scope.secondarySkillStyle = [];
    $scope.ratiosToDisplay = [];

    secondaryBoxColors = ['#D6FFEB', '#C2FFE0', '#ADFFD6', '#99FFCC', '#7ACCA3', '#5C997A', '#3D6652'];

    $scope.primarySkillsPerPage = 20; // this should match however many results your API puts on one page
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
		  /************
		  var width = skill.associated_terms[j].ratio * 7000;
		  var sqRootWidth = Math.floor(Math.sqrt(width));
		  var computedSideX = width;
		  var computedSideY = 50;
		  if (sqRootWidth > 100) {
		    computedSideX = sqRootWidth;
		    computedSideY = sqRootWidth;
		  }
		  //var remainderWidth = width;
		  var remainderWidth = computedSideX;
		  var previousRemainderWidth = remainderWidth;
		  ************/
		  var computedSideX = 150;
		  var computedSideY = 50;
		  var height = 30;
		  var padding = 0;
		  var fontSize = 100;
		  var fontSizeFactor = 1;
		  var paddingIncrease = 0;
		  var padding = 0;
		  var wordBreak = 'normal';
		  var boxColor = '#D6FFEB';
		  var ratio = skill.associated_terms[j].ratio;
		  if (skill.associated_terms[j].ratio < 0.01) {
		    //ratioToDisplay = "< 0.01";
		    $scope.ratiosToDisplay[i][j] = "< 0.01";
		  }
		  else {
		    //ratioToDisplay = skill.associated_terms[j].ratio.toFixed(2);
		    var ratioAsNumber = Number.parseFloat(ratio);
		    $scope.ratiosToDisplay[i][j] = ratioAsNumber.toFixed(2);
		  }

		  var fontScaleFactor = 1;
		  var colorIndex = 0;
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

		  var boxScaleFactorX = 1;
		  var boxScaleFactorY = 1;
		  var fontScaleFactor = 1;

		  //if (computedSideX > 200) {
		    var percentage = ratio * 100;
		    switch (Math.floor(percentage / 10)) {
		    case 1: 
		      boxScaleFactorX = 1.1;
		      break;
		    case 2: 
		      boxScaleFactorX = 1.2;
		      boxScaleFactorY = 1.1;
		      fontScaleFactor = 1.1;
		      colorIndex = 1;
		      break;
		    case 3: 
		      boxScaleFactorX = 1.3;
		      boxScaleFactorY = 1.1;
		      fontScaleFactor = 1.1;
		      colorIndex = 1;
		      break;
		    case 4: 
		      boxScaleFactorX = 1.4;
		      boxScaleFactorY = 1.2;
		      fontScaleFactor = 1.2;
		      colorIndex = 2;
		      break;
		    case 5: 
		      boxScaleFactorX = 1.5;
		      boxScaleFactorY = 1.2;
		      fontScaleFactor = 1.2;
		      colorIndex = 2;
		      break;
		    case 6: 
		      boxScaleFactorX = 1.6;
		      boxScaleFactorY = 1.3;
		      fontScaleFactor = 1.3;
		      colorIndex = 3;
		      break;
		    case 7: 
		      boxScaleFactorX = 1.7;
		      boxScaleFactorY = 1.3;
		      fontScaleFactor = 1.3;
		      colorIndex = 3;
		      break;
		    case 8: 
		      boxScaleFactorX = 1.8;
		      boxScaleFactorY = 1.4;
		      fontScaleFactor = 1.4;
		      colorIndex = 4;
		      break;
		    case 9: 
		      boxScaleFactorX = 1.9;
		      boxScaleFactorY = 1.4;
		      fontScaleFactor = 1.4;
		      colorIndex = 4;
		      break;
		    case 10: 
		      boxScaleFactorX = 2.0;
		      boxScaleFactorY = 1.5;
		      fontScaleFactor = 1.5;
		      colorIndex = 5;
		      break;
 		    default: 
		      break;
		    }


		    /*************
		    var boxSizeFactor = computedSideX / 200;
		    var colorIndex = Math.floor(boxSizeFactor / 2);
		    if (colorIndex > secondaryBoxColors.length - 1) {
		      //console.log("colorIndex = " + colorIndex + " larger than secondaryBoxColors.length - 1");
		      colorIndex = secondaryBoxColors.length - 1;
		    }
		    *********/
		    boxColor = secondaryBoxColors[colorIndex];
		    //var boxScaleFactor = 0.02 * boxSizeFactor;
		    //var fontScaleFactor = 1 + 0.1 * boxSizeFactor;
		    computedSideX = Math.floor(computedSideX * boxScaleFactorX);
		    computedSideY = Math.floor(computedSideY * boxScaleFactorX);

		    //computedSideX = Math.floor(200 + 100 * boxScaleFactor);
		    //computedSideY = Math.floor(computedSideX * 0.75);
		    //paddingIncrease = Math.floor(boxSizeFactor * 1.05);
		    wordBreak = 'break-all';
		  //}

		  //previousRemainderWidth = previousRemainderWidth + "px";
		  height = height + "px";
		  fontSize = Math.floor(fontScaleFactor * 100) + "%";
		  //padding = paddingIncrease + "% 0%";
		  //padding = paddingIncrease + "% 0%";
		  computedSideX = computedSideX + "px";
		  computedSideY = computedSideY + "px";
		    
		  
		  //$scope.secondarySkillStyle[i][j] = {'width': previousRemainderWidth, 'height': height, 'background-color': '#C2FFC2', 'margin':'5px 0px', 'padding': padding, 'text-align': 'center', 'fontSize': fontSize };
		  //$scope.secondarySkillStyle[i][j] = {'width': computedSide, 'height': computedSide, 'background-color': '#C2FFC2', 'margin':'5px 0px', 'padding': padding, 'text-align': 'center', 'fontSize': fontSize, 'word-break': wordBreak };
		  $scope.secondarySkillStyle[i][j] = {'width': computedSideX, 'height': computedSideY, 'background-color': boxColor, 'margin':'5px 0px', 'text-align': 'center', 'fontSize': fontSize, 'word-break': wordBreak };
                }
            }

        });
  };

  $scope.setShowAssociatedSkills = function (i) {
    $scope.showAssociatedSkills[i] = !$scope.showAssociatedSkills[i];
  }

}]);
