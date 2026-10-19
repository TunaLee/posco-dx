import { test } from "node:test";
import assert from "node:assert";
import { settle, check } from "../src/settle.js";
import { page } from "../src/paging.js";

test("정산액 계산", () => {
  assert.equal(settle({ distance: 100, weight: 10, unitPrice: 180 }), 180000);
});

test("10% 과다 청구는 이의 제기", () => {
  assert.equal(check({ distance: 100, weight: 10, unitPrice: 180, billed: 198000 }).dispute, true);
});

test("소수 중량", () => {
  assert.equal(settle({ distance: 333, weight: 5.5, unitPrice: 185 }), 338846);
});

test("첫 페이지", () => {
  assert.equal(page([1, 2, 3, 4, 5], 1, 2)[0], 1);
});
