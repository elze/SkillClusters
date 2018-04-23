app.service('statCounterService', [function () {

        this.postscribeStatcounter = function () {
	  sc_project="*****"; // redacted, since it includes my personal information
	  sc_invisible=1;
	  sc_security="***";  // redacted, since it includes my personal information

	  var scURL = 'http://www.statcounter.com/counter/counter.js';

	  var scImg = '***';  // redacted, since it includes my personal information
	  angular.element(document.getElementById('statcounterInd')).empty();
	  postscribe('#statcounterInd', '<script src="' + scURL + '"><img class="statcounter" src="' + scImg + '" alt="free hit counter"><\/script>');
        };
}]);
