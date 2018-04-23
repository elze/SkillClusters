app.service('scModalService', ['$uibModal', '$rootScope', 'statCounterService', 'iconService',
			       function ($uibModal, $rootScope, statCounterService, iconService) {

        this.showModal = function (primary_term, secondary_term, skill_pair_id) {
	  var modalOptions = {
	  controller: function($scope, $http) {
	      $http.get('jobsPerSkillPair/' + skill_pair_id).then(function (result) {
		  $scope.current_primary_term = primary_term;
		  $scope.current_secondary_term = secondary_term;
		  $scope.current_skill_pair_id = skill_pair_id;
		  $scope.jobSnippets = result;
		  let indexOfExistingSnippet = $rootScope.pageTitle.indexOf(' ; job snippets: ');
		  if (indexOfExistingSnippet != -1) {
		    $rootScope.pageTitle = $rootScope.pageTitle.substring(0, indexOfExistingSnippet);
		  }
		  $rootScope.pageTitle = $rootScope.pageTitle + ' ; job snippets: ' + primary_term + ' / ' + secondary_term;
		  statCounterService.postscribeStatcounter();
		  iconService.removeSpinner(secondary_term);
		});
	      $scope.getJobPostingRoute = function(jobFileName, primary_term, secondary_term) {
		let indexOfDot = jobFileName.indexOf(".");
		let jobPostingRoute = jobFileName.substring(0, indexOfDot);
		return `jobPosting/${jobPostingRoute}/${primary_term}/${secondary_term}`;
	      }
	      $scope.jobSnippetsPerPage = 8;
	    },
	templateUrl: 'views/jobSnippetsModal.html'
	  };
            return $uibModal.open(modalOptions).result;
        };
					   }]);
