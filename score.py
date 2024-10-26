import json

def load_json(file_path):
    """
    載入 JSON 檔案。
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def compare_predictions(ground_truths, predictions):
    """
    比較預測結果與正確答案，計算準確率並找出差異。
    """
    correct = 0
    total = len(ground_truths['ground_truths'])
    differences = []

    # 將 ground truths 和 predictions 轉換為以 qid 為鍵的字典
    gt_dict = {item['qid']: item for item in ground_truths['ground_truths']}
    pred_dict = {item['qid']: item for item in predictions['answers']}

    for qid, gt in gt_dict.items():
        pred = pred_dict.get(qid)
        if pred:
            if gt['retrieve'] == pred['retrieve']:
                correct += 1
            else:
                differences.append({
                    'qid': qid,
                    'ground_truth': gt['retrieve'],
                    'prediction': pred['retrieve'],
                    'category': gt['category']
                })
        else:
            differences.append({
                'qid': qid,
                'ground_truth': gt['retrieve'],
                'prediction': None,
                'category': gt['category']
            })

    accuracy = (correct / total) * 100
    return accuracy, differences

def main():
    """
    主函式，執行比對並輸出結果。
    """
    ground_truths = load_json('dataset/preliminary/ground_truths_example.json')
    predictions = load_json('dataset/preliminary/pred_retrieve.json')

    accuracy, differences = compare_predictions(ground_truths, predictions)

    print(f"整體準確率: {accuracy:.2f}%")
    print(f"總共 {len(ground_truths['ground_truths'])} 筆資料")
    print(f"正確預測: {int((accuracy/100)*len(ground_truths['ground_truths']))} 筆")
    print(f"錯誤預測: {len(differences)} 筆\n")

    if differences:
        print("預測錯誤的項目:")
        for diff in differences:
            print(f"QID {diff['qid']}: 正確值 = {diff['ground_truth']}, 預測值 = {diff['prediction']}, 類別 = {diff['category']}")

if __name__ == "__main__":
    main()
