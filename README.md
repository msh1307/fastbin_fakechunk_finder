# fastbin_fakechunk_finder
glibc with no 0x10 alignment validation in fastbin range.
```
gef➤  source ./fastbin_fakechunk_finder/script.py
addr hex: 0x0000000000602000
len hex: 0x1000
found sz :  0x60
malloc sz : 0x50
addr : 0x601ffa
found sz :  0x40
malloc sz : 0x30
addr : 0x602012
found sz :  0x40
malloc sz : 0x30
addr : 0x60201a
found sz :  0x40
malloc sz : 0x30
addr : 0x602022
found sz :  0x40
malloc sz : 0x30
addr : 0x60202a
found sz :  0x40
malloc sz : 0x30
addr : 0x602032
found sz :  0x40
malloc sz : 0x30
addr : 0x602042
found sz :  0x40
malloc sz : 0x30
addr : 0x60204a
found sz :  0x40
malloc sz : 0x30
addr : 0x602052
found sz :  0x40
malloc sz : 0x30
addr : 0x60205a
found sz :  0x40
malloc sz : 0x30
addr : 0x602062
found sz :  0x40
malloc sz : 0x30
addr : 0x60206a
found sz :  0x40
malloc sz : 0x30
addr : 0x602072
found sz :  0x78
malloc sz : 0x60
addr : 0x60209d
found sz :  0x78
malloc sz : 0x60
addr : 0x6020ad
```
glibc 2.23
```
#define fastbin_index(sz) \
  ((((unsigned int) (sz)) >> (SIZE_SZ == 8 ? 4 : 3)) - 2)
#define SIZE_BITS (PREV_INUSE | IS_MMAPPED | NON_MAIN_ARENA)

/* Get size, ignoring use bits */
#define chunksize(p)         ((p)->size & ~(SIZE_BITS))


  if ((unsigned long) (nb) <= (unsigned long) (get_max_fast ()))
    {
      idx = fastbin_index (nb);
      mfastbinptr *fb = &fastbin (av, idx);
      mchunkptr pp = *fb;
      do
        {
          victim = pp;
          if (victim == NULL)
            break;
        }
      while ((pp = catomic_compare_and_exchange_val_acq (fb, victim->fd, victim))
             != victim);
      if (victim != 0)
        {
          if (__builtin_expect (fastbin_index (chunksize (victim)) != idx, 0))
            {
              errstr = "malloc(): memory corruption (fast)";
            errout:
              malloc_printerr (check_action, errstr, chunk2mem (victim), av);
              return NULL;
            }
          check_remalloced_chunk (av, victim, nb);
          void *p = chunk2mem (victim);
...
```
