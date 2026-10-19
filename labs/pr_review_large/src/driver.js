// 사내 DB 드라이버 래퍼
export async function query(sql, params = []) {
  throw new Error("DB 연결 없음: " + sql.slice(0, 40) + " " + params.length);
}
