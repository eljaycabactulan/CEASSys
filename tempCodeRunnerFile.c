#include <stdio.h>

void swap(int* a, int* b){
    int temp = *a;
    *a = *b;
    *b = temp;
}

int partition(int arr[], int low, int high){
    int p = arr[low];
    int i = low;
    int j = high;
    
    while(i<j){
        while (arr[i] <= p && i <= high -1){
            i++;
        }
        while (arr[j] >= p && j >= low + 1){
            j--;
        }
        if (i<j){
        swap(&arr[i], &arr[j]);
        }
    }
    
    swap(&arr[j], &arr[low]);
    return j;
 
}

void quicksrt(int arr[], int low, int high){
    if(low<high){
        int p = partition(arr, low, high);
        quicksrt(arr, low, p -1);
        quicksrt(arr, p + 1, high);
    }
}

int main(){
    int arr[] = {4,3,6,8,7};
    int n = sizeof(arr)/sizeof(arr[0]);
    
    quicksrt(arr, 0, n-1);
    
    for(int i = 0; i < n; i++){
        printf("%d,", arr[i]);
    }
    
}