app.service('scModalService', ['$uibModal',
    function ($uibModal) {

        this.showModal = function (primary_term, secondary_term, skill_pair_id) {
	  var modalOptions = {
	  controller: function($scope) {
	      $scope.current_primary_term = primary_term;
	      $scope.current_secondary_term = secondary_term;
	      $scope.current_skill_pair_id = skill_pair_id;
	    }
	templateUrl: 'views/jobSnippetsModal.html'
	  };
            return $uibModal.open(modalOptions).result;
        };
					   }]);
