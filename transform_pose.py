
import pandas as pd
import sys

def transform_data(data, first_index, first_range, second_index, second_range):
    def apply_transformation(index, range_val):
        start = index - range_val
        forward = list(range(start+1, start + 2 * range_val+1))
        backward = list(range(start + 2 * range_val - 1, start - 1, -1))
        transform_list = forward + backward + forward
        transform_list.insert(0,start)  
        return transform_list  # 순차, 역순, 다시 순차로 적용
    
    first_transformation = apply_transformation(first_index, first_range)
    second_transformation = apply_transformation(second_index, second_range)
    
    transformed_indices = list(range(0, first_index - first_range)) + first_transformation + \
                          list(range(first_index+first_range+1, second_index - second_range)) + second_transformation + \
                          list(range(second_index+first_range+1, len(data)))
    
    # 첫 번째 변환과 두 번째 변환에서 추가 움직임이 생기므로, 원래 데이터의 처음과 마지막에서 그만큼을 제거
    start_remove = first_range * 4
    end_remove = len(transformed_indices) - 4 * second_range
    
    transformed_data = data.iloc[transformed_indices[start_remove:end_remove]].reset_index(drop=True)
    
    return transformed_data

if __name__ == "__main__":
    if len(sys.argv) != 7:
        print("Usage: python transform_pose.py <input_file> <first_index> <first_range> <second_index> <second_range> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    first_index = int(sys.argv[2])
    first_range = int(sys.argv[3])
    second_index = int(sys.argv[4])
    second_range = int(sys.argv[5])
    output_file = sys.argv[6]

    data = pd.read_csv(input_file)
    transformed_data = transform_data(data, first_index, first_range, second_index, second_range)
    transformed_data.to_csv(output_file, index=False)
