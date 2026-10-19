import java.util.*;

class Solution {
    public List<Integer> targetIndices(int[] nums, int target) {
        Arrays.sort(nums);
        List<Integer> list = new ArrayList<>();
        for(int i = 0; i < nums.length; i++)
        {
            if(nums[i] == target)
            {
                list.add(i);
            }
        }
        return list;
    }

    public List<Integer> targetIndices(int[] nums, int target) {
        int small_count = 0;
        int target_count = 0;
        List<Integer> list = new ArrayList<>();
        for(int i = 0; i < nums.length; i++)
        {
            if(nums[i] == target)
            {
                target_count++;
            }
            if(nums[i] < target)
            {
                small_count++;
            }
        }
        for(int i = 1; i <= target_count; i++)
        {
            list.add(small_count++);
        }
        return list;
    }
}

