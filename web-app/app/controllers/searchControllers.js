'use strict';


angular.module('angApp.searchControllers', ['angApp.appConfig'])

 .controller('SearchCtrl', ['$scope', '$rootScope', '$interval', '$window', '$http', 'ENV', 'Search',
    function($scope, $rootScope, $interval, $window, $http, ENV, Search) {

    $scope.params = {
        
        SearchType: null
    };
        
    $scope.environmentURL = null;
    
    var poll;
        
    $scope.searchResults = null;
    $scope.images = null;
    $scope.titles = null;

    checkForSearchResults();
        
    function checkForSearchResults() {
        
        // poll every few seconds for new search results i.e. matches
        poll = $interval( () => { 

            // placeholder, no need yet for params for API call
            let params = {
                ApiCallType: "check-search-results"
            }

            $http.post(ENV + 'matches', params)

                 .then(

                   // backend responded successfully
                   function(response) {

                        console.log(response);
                        let rawResult = response.data.body;
                        rawResult = rawResult.replace(/\'/g, "\"");
                        let json = JSON.parse(rawResult);
                        $scope.searchResults = json;

                        $scope.images = [];
                        $scope.titles = [];
                        let matches = json.matches;
                        matches.forEach( match => {
                            $scope.images.push(match.url);
                            $scope.titles.push(match.title);
                        });

                   }, 
                   // failure outside the backend function, e.g. couldn't call the backend
                   function(response) {
                       
                        $scope.stop();
                        console.log(response);
                   }       
            );  
            
        }, 10000); // end poll
                
    }
    
    $scope.stop = () => {
        
        if (angular.isDefined(poll)) {
              
            $interval.cancel(poll);
            poll = undefined;
        }
    };
    
    $scope.$on('$destroy', ()  => {
        
        // make sure that the interval also is destroyed
        $scope.stop();
    });
    
    // the API call below is a form that can be used for single calls,
    // rather than for polling
    /*
    Search.result.searchResults($scope.params.SearchType, function(data) {

        console.log(data);
        $scope.searchResults = data.body

    }, function(e) {

        console.log(e);
    } );
    */

}]);

