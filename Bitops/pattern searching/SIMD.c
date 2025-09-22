for (i = 0; i < n; i += w)
{
    load text window into SIMD register compare bytes against pattern
        use movemask to find byte positions that match if match (s),
        verify exact match as needed
}