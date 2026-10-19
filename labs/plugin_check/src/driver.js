// 사내 DB 드라이버 래퍼 (테스트에서는 가짜로 바꿈)
export async function query(sql) {
  throw new Error("DB 연결 없음: " + sql.slice(0, 40));
}
