app.service('iconService', ['$rootScope', function ($rootScope) {
      var secondaryExpandableClass = "fas fa-expand fa-xs";
      var secondarySpinnerClass = "fas fa-spinner fa-spin fa-3x";
      this.associatedSkillsIcons = {};
      this.initializeAssociatedSkillsIcons = function (skill) {
	var associatedSkillsIcons = {};
	skill.associated_terms.map(x => 
	    this.associatedSkillsIcons[x.secondary_term] = secondaryExpandableClass
	    );
	return this.associatedSkillsIcons;
      }

        this.setSpinner = function (secondary_term) {
	  this.associatedSkillsIcons[secondary_term] = secondarySpinnerClass;
	}

        this.removeSpinner = function (secondary_term) {
	  this.associatedSkillsIcons[secondary_term] = secondaryExpandableClass;
	}
    }]);
