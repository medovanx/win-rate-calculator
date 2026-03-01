(function () {
  var form = document.getElementById('calculator');
  var resultEl = document.getElementById('result');
  var matchesInput = document.getElementById('matches');
  var winrateInput = document.getElementById('winrate');
  var expectedWrInput = document.getElementById('expected-wr');

  function showResult(message, type) {
    resultEl.textContent = message;
    resultEl.className = 'result ' + type;
  }

  function calculate() {
    var matchesRaw = matchesInput.value.trim();
    var winrateRaw = winrateInput.value.trim();
    var expectedWrRaw = expectedWrInput.value.trim();

    if (!matchesRaw || !winrateRaw || !expectedWrRaw) {
      showResult('Enter valid values.', true);
      return;
    }

    var matches = parseInt(matchesRaw, 10);
    var winrate = parseFloat(winrateRaw);
    var expectedWr = parseFloat(expectedWrRaw);

    if (Number.isNaN(matches) || Number.isNaN(winrate) || Number.isNaN(expectedWr)) {
      showResult('Enter valid values.', 'error');
      return;
    }

    if (matches < 1) {
      showResult('Enter valid values.', 'error');
      return;
    }

    if (winrate < 0 || winrate > 100 || expectedWr < 0 || expectedWr > 100) {
      showResult('Enter valid values.', 'error');
      return;
    }

    var currentWR = winrate / 100;
    var expectedWR = expectedWr / 100;

    if (expectedWR > currentWR) {
      if (expectedWR >= 1) {
        showResult('Not achievable.', 'error');
        return;
      }
      var x = (matches * (expectedWR - currentWR)) / (1 - expectedWR);
      var count = Math.ceil(x);
      if (count < 0 || !Number.isFinite(count)) {
        showResult('Enter valid values.', 'error');
        return;
      }
      showResult('You need to win ' + count + ' consecutive matches.', 'success');
      return;
    }

    if (expectedWR < currentWR) {
      if (expectedWR <= 0) {
        showResult('Not achievable.', 'error');
        return;
      }
      var xLosses = (matches * (currentWR - expectedWR)) / expectedWR;
      var countLosses = Math.ceil(xLosses);
      if (countLosses < 0 || !Number.isFinite(countLosses)) {
        showResult('Enter valid values.', 'error');
        return;
      }
      showResult('You need to lose ' + countLosses + ' consecutive matches.', 'loss');
      return;
    }

    showResult("You're already at this winrate.", 'success');
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    calculate();
  });
})();
