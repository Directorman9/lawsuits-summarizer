packages.controller('packages_ctrl',function($scope, $http){  

 
        

        $scope.init = function(){
            $scope.show_standard = 0;

        } 

        $scope.get_data = function(id, amount){

            if (id == 0) {
               $scope.show_standard = 1; 
               $scope.show_custom = 0; 
               get_moderate_data(amount);
            }
            else if (id == 1) {
               $scope.show_standard = 1;
               $scope.show_custom = 0;  
               get_classic_data(amount);
            }
            else if (id == 2){
               $scope.show_standard = 1; 
               $scope.show_custom = 0; 
               get_premium_data(amount);
            } 
            else if (id == 3){
               $scope.show_standard = 0; 
               $scope.show_custom = 1; 
               get_custom_data();
            } 

        };

        get_moderate_data = function(amount){
            $http.get('/get_moderate_data')
                 .then(function(resp) {
                     $scope.data = resp.data;
                     $scope.data.cost = amount;

                 })
                 .catch(function(err){
                     $scope.errmsg = "server error";
                 });
                 
        };

        
        get_classic_data = function(amount){ 
            $http.get('/get_classic_data')
                .then(function(resp) {
                    $scope.data = resp.data;
                    $scope.data.cost = amount;
                }) 
                .catch(function(err){
                    $scope.errmsg = "server error";
                });
                 
        };


        get_premium_data = function(amount){
            $http.get('/get_premium_data')
                .then(function(resp) {
                    $scope.data = resp.data;
                    $scope.data.cost = amount;
                })
                .catch(function(err){
                    $scope.errmsg = "server error";
                });
                 
        };


        get_custom_data = function(amount){
            $http.get('/get_custom_data')
                .then(function(resp) {
                    $scope.data = resp.data;
                })
                .catch(function(err){
                    $scope.errmsg = "server error";
                });
                 
        };






});