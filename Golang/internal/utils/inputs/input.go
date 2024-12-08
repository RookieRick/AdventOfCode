package inputs

import (
	"bufio"
	"errors"
	"io"
	"net/http"
	"net/http/cookiejar"
	"net/url"
	"os"
	"path/filepath"
	"strings"
)

// GetInput will.. well.. get the input.
// Massive caveat: It assumes executable is in e.g.  cmd/2022/day/1 which just so happens
// to be the case when running in VSCode debugger which is the only place I run these. YMMV
func GetInput(prefix ...string) ([]string, error) {

	var (
		err        error
		executable string
		fp         *os.File
	)

	if executable, err = os.Executable(); err != nil {
		return nil, err
	}

	dir, _ := filepath.Split(executable)

	cacheDir := filepath.Join(dir, "_input_cache")

	sliced := strings.Split(strings.TrimRight(filepath.ToSlash(dir), "/"), "/")
	year := sliced[len(sliced)-3]
	day := sliced[len(sliced)-1]

	os.MkdirAll(cacheDir, 0700) // will create dir if doesn't exist, else NOOP

	fileNameParts := append(prefix, "raw_input.txt")

	cacheFile := filepath.Join(cacheDir, strings.Join(fileNameParts, "_"))
	fp, err = os.OpenFile(cacheFile, os.O_RDWR, 0600)
	if errors.Is(err, os.ErrNotExist) {
		// file not found - create it, retrieve input from web and reset our fp to prep for read
		if fp, err = os.OpenFile(cacheFile, os.O_RDWR|os.O_CREATE, 0600); err != nil {
			return nil, err
		}
		inputUrl := &url.URL{
			Scheme: "https",
			Host:   "adventofcode.com",
			Path:   year + "/day/" + day + "/input",
		}
		http.DefaultClient.Jar, _ = cookiejar.New(nil)
		http.DefaultClient.Jar.SetCookies(inputUrl, []*http.Cookie{{
			Name:  "session",
			Value: os.Getenv("AOC_SESSION_TOKEN"),
		}})

		if resp, err := http.Get(inputUrl.String()); err != nil {
			return nil, err
		} else {
			defer resp.Body.Close()
			if resp.StatusCode == 404 {
				_ = fp.Close()
				os.Remove(cacheFile)
				return nil, errors.New("failed to retrieve input with 404 -- too early?")
			}
			if _, copyErr := io.Copy(fp, resp.Body); copyErr != nil {
				return nil, copyErr
			}
		}
		fp.Seek(0, 0) // move read head back to start
	}
	defer fp.Close()

	fileScanner := bufio.NewScanner(fp)
	fileScanner.Split(bufio.ScanLines)
	var fileLines []string
	for fileScanner.Scan() {
		fileLines = append(fileLines, fileScanner.Text())
		// TODO: apply transforms if you decide you want to use sim approach to your Python version
	}

	return fileLines, nil
}
