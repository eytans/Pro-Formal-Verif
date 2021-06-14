;; tot = *
;; do
;;   if (lck == 0) lck = 1;
;;   old = tot
;;   req = *;
;;   if (req)
;;     if (lck==1) lck = 0;
;;     tot = tot+1;
;; while (tot != old)
;; if (lck == 0) error();

(declare-rel PreLoop (Int Int Int))
(declare-rel PostLoop (Int Int Int))
(declare-rel Error ())

(declare-rel P1 (Int Int))
(declare-rel P0 (Int))

(declare-var tot Int)
(declare-var old Int)
(declare-var tot_p Int)
(declare-var old_p Int)
(declare-var req Bool)
(declare-var lck Int)
(declare-var lck_0 Int)
(declare-var lck_1 Int)

;; tot = *
;; do
;;   if (lck == 0) lck = 1;
;;   old = tot
;;   req = *;
;;   if (req)
;;     if (lck==1) lck = 0;
;;     tot = tot+1;
;; while (tot != old)
;; if (lck == 0) error();

(declare-rel Init (Int Int Int))

;; write constraints for the above program
;;(rule (=> (P0 lck) (PreLoop lck old tot)))
(rule (Init lck old tot))
(rule (=> (and (= lck 0) (Init lck old tot) (= tot_p (+ 1 tot))) (PostLoop 0 tot tot_p)))
(rule (=> (and (= lck 0) (Init lck old tot)) (PostLoop 1 tot tot)))
(rule (=> (and (not (= lck 0)) (Init lck old tot)) (PostLoop lck tot tot)))
(rule (=> (and (= lck 0) (PreLoop lck old tot) (= tot_p (+ 1 tot))) (PostLoop 0 tot tot_p)))
(rule (=> (and (= lck 0) (PreLoop lck old tot)) (PostLoop 1 tot tot)))
(rule (=> (and (not (= lck 0)) (PreLoop lck old tot)) (PostLoop lck tot tot)))
(rule (=> (and (PostLoop lck old tot) (not (= old tot))) (PreLoop lck old tot)))
(rule (=> (and (PostLoop lck old tot) (= old tot) (= lck 0)) Error))
(query Error)