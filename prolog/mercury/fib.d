

fib.optdate fib.trans_opt_date ./fib.err fib.c_date fib.s_date fib.pic_s_date fib.il_date fib.java_date : ./fib.m

fib.mh fib.mih : fib.c


ifeq ($(findstring il,$(GRADE)),il)
fib.module_dep : fib.il
else
 ifeq ($(findstring java,$(GRADE)),java)
fib.module_dep : jmercury/fib.java
 else
fib.module_dep : fib.c
 endif
endif


fib.date fib.date0 : ./fib.m

fib.date0 : ./fib.m


fib.int0 : fib.date0
	@:
fib.int : fib.date
	@:
fib.int2 : fib.date
	@:
fib.int3 : fib.date3
	@:
fib.opt : fib.optdate
	@:
fib.trans_opt : fib.trans_opt_date
	@:

fib.date0 : ./fib.m
	$(MCPI) $(ALL_GRADEFLAGS) $(ALL_MCPIFLAGS) ./fib.m
fib.date : ./fib.m
	$(MCI) $(ALL_GRADEFLAGS) $(ALL_MCIFLAGS) ./fib.m
fib.date3 : ./fib.m
	$(MCSI) $(ALL_GRADEFLAGS) $(ALL_MCSIFLAGS) ./fib.m
fib.optdate : ./fib.m
	$(MCOI) $(ALL_GRADEFLAGS) $(ALL_MCOIFLAGS) ./fib.m
fib.trans_opt_date : ./fib.m
	$(MCTOI) $(ALL_GRADEFLAGS) $(ALL_MCTOIFLAGS) ./fib.m
fib.c_date : ./fib.m
	$(MCG) $(ALL_GRADEFLAGS) $(ALL_MCGFLAGS) ./fib.m $(ERR_REDIRECT)
fib.il_date : ./fib.m
	$(MCG) $(ALL_GRADEFLAGS) $(ALL_MCGFLAGS) --il-only ./fib.m $(ERR_REDIRECT)
fib.java_date : ./fib.m
	$(MCG) $(ALL_GRADEFLAGS) $(ALL_MCGFLAGS) --java-only ./fib.m $(ERR_REDIRECT)
