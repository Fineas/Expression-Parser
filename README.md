# Expression-Parser

## Vocabulary of Propositional Logic

*Countable Set*
> A, B, F, G, H, P, Q, R, F1 ... Fn ...

*Logical Connections*
> ! (not), & (and), | (or), > (implication), ~ (equivalent)

## Expressions of Propositional Logic
*if P,Q ∈ P(v) then:*

> (!P) ∈ P(v), the nagation of P

> (P & Q) ∈ P(v), the conjunctions of P,Q

> (P | Q) ∈ P(v), the disjunction of P,Q

> (P > Q) ∈ P(v), the implication between P,Q

> (P ~ Q) ∈ P(v), the equivalence of P,Q

## Valid Examples
> (P - (Q & R))

> A

> (P&((!Q)&(!(!(Q~(!R))))))

![first exmaple](https://raw.githubusercontent.com/Fineas/Expression-Parser/master/img/example1.png)

## Interpretation

> A = True, B = True, C = True, D = False
> (A & (B | (C & (!D))))
> (True & (True | (True & (!False))))
> (True & (True | (True & True)))
> (True & (True | True))
> (True & True)
> True

## Note
*This program was designed in order to automatically solve similar excercises (homework assignment).*  
