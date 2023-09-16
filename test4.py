import multiprocessing

# 각 프로세스에서 수행할 작업을 정의하는 함수
def square_number(number):
    result = number * number
    print(f"{number}의 제곱은 {result}입니다.")

if __name__ == "__main__":
    # 병렬 처리할 데이터 리스트
    numbers = [1, 2, 3, 4, 5, 6, 7, 8]

    # 사용 가능한 코어 수만큼 프로세스 풀 생성
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

    # 각 숫자를 제곱하는 함수를 프로세스에 할당하여 병렬로 실행
    pool.map(square_number, numbers)

    # 작업 완료 후 풀 종료
    pool.close()
    pool.join()